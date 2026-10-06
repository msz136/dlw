using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Globalization;
using System.IO;
using System.Net;
using System.Net.Sockets;
using System.Reflection;
using System.Security.Cryptography;
using System.Text;
using System.Text.RegularExpressions;
using System.Threading;
using System.Web.Script.Serialization;
using System.Windows.Forms;

[assembly: AssemblyTitle("Report")]
[assembly: AssemblyDescription("Open the local academic report and its notebook service")]
[assembly: AssemblyCompany("ACA")]
[assembly: AssemblyProduct("Report")]
[assembly: AssemblyVersion("1.0.0.0")]
[assembly: AssemblyFileVersion("1.0.0.0")]

internal static class ReportLauncher
{
    private const string ServiceName = "aca-report-notebook";
    private static readonly JavaScriptSerializer Json = new JavaScriptSerializer();
    private static readonly string ProjectRelative = Path.Combine("Workspaces", "report_notebook_20261002");
    private static string logPath;
    private static string outcomePath;

    // The child owns its log handles and keeps them after this GUI launcher exits.
    // No shell, terminal, .cmd file or separate bootstrap file is involved.
    private const string Bootstrap =
        "import os,runpy,sys\n" +
        "server_path,port,log_path=sys.argv[1:4]\n" +
        "sys.stdout=open(log_path,'a',encoding='utf-8',buffering=1)\n" +
        "sys.stderr=sys.stdout\n" +
        "sys.path.insert(0,os.path.dirname(server_path))\n" +
        "sys.argv=[server_path,'--port',port]+sys.argv[4:]\n" +
        "runpy.run_path(server_path,run_name='__main__')\n";

    [STAThread]
    private static int Main(string[] args)
    {
        bool noOpen = false;
        int port = 8766;
        string idleSeconds = null;
        Mutex launchMutex = null;
        bool ownsMutex = false;
        try
        {
            for (int i = 0; i < args.Length; ++i)
            {
                if (args[i] == "--no-open") noOpen = true;
                else if (args[i] == "--port" && i + 1 < args.Length)
                    port = int.Parse(args[++i], CultureInfo.InvariantCulture);
                else if (args[i] == "--idle-seconds" && i + 1 < args.Length)
                    idleSeconds = int.Parse(args[++i], CultureInfo.InvariantCulture).ToString(CultureInfo.InvariantCulture);
                else throw new InvalidOperationException("无法识别启动参数：" + args[i]);
            }
            if (port < 1024 || port > 65535) throw new InvalidOperationException("报告端口无效。");
            string workspace = FindWorkspace(AppDomain.CurrentDomain.BaseDirectory);
            string project = Path.Combine(workspace, ProjectRelative);
            string package = Path.Combine(project, "package");
            string logs = Path.Combine(package, "logs");
            Directory.CreateDirectory(logs);
            string stamp = DateTime.UtcNow.ToString("yyyyMMdd_HHmmss_fff", CultureInfo.InvariantCulture) + "_" + Process.GetCurrentProcess().Id;
            logPath = Path.Combine(logs, "launcher_" + stamp + ".log");
            outcomePath = Path.Combine(logs, "launcher_" + stamp + ".json");
            string script = Path.Combine(project, "runtime", "report_server.py");
            string version = ExpectedVersion(script);
            string serviceUrl = "http://127.0.0.1:" + port.ToString(CultureInfo.InvariantCulture);
            string mutexName = "Local\\ACAReportLauncher-" + Digest(workspace.ToLowerInvariant()) + "-" + port;
            launchMutex = new Mutex(false, mutexName);
            try { ownsMutex = launchMutex.WaitOne(TimeSpan.FromSeconds(60)); }
            catch (AbandonedMutexException) { ownsMutex = true; }
            if (!ownsMutex) throw new InvalidOperationException("另一个报告窗口正在启动，请稍后再打开。");
            WriteLog("Checking report service at " + serviceUrl + "; expected " + version);

            Dictionary<string, object> health = Health(serviceUrl);
            for (int n = 0; health != null && StringValue(health, "status") == "stopping" && n < 120; ++n)
            {
                Thread.Sleep(250);
                health = Health(serviceUrl);
            }
            bool started = false;
            bool migrated = false;
            string python = null;
            string serverLog = null;
            if (health != null && StringValue(health, "service") == ServiceName && StringValue(health, "version") != version)
            {
                MigrateIdleService(health, workspace, script, serviceUrl, port);
                health = null;
                migrated = true;
            }
            if (health != null)
            {
                VerifyHealth(health, version, workspace, script, port);
                WriteLog("Reusing ready report service PID " + StringValue(health, "pid"));
            }
            else
            {
                if (PortOpen(port)) throw new InvalidOperationException("报告端口 " + port + " 正被其他程序占用，无法打开报告。");
                python = FindPython();
                serverLog = Path.Combine(logs, "service_" + stamp + ".log");
                ProcessStartInfo start = new ProcessStartInfo();
                start.FileName = python;
                start.Arguments = "-u -c " + Quote(Bootstrap) + " " + Quote(script) + " " + Quote(port.ToString(CultureInfo.InvariantCulture)) + " " + Quote(serverLog);
                if (idleSeconds != null) start.Arguments += " --idle-seconds " + Quote(idleSeconds);
                start.WorkingDirectory = workspace;
                start.UseShellExecute = false;
                start.CreateNoWindow = true;
                start.WindowStyle = ProcessWindowStyle.Hidden;
                start.EnvironmentVariables["PYTHONUTF8"] = "1";
                using (Process child = Process.Start(start))
                {
                    if (child == null) throw new InvalidOperationException("报告服务未能启动。");
                    WriteLog("Started hidden Python report service PID " + child.Id + "; log " + serverLog);
                    Stopwatch timer = Stopwatch.StartNew();
                    while (timer.Elapsed < TimeSpan.FromSeconds(45))
                    {
                        Thread.Sleep(200);
                        health = Health(serviceUrl);
                        if (health != null)
                        {
                            VerifyHealth(health, version, workspace, script, port);
                            started = true;
                            break;
                        }
                        if (child.HasExited)
                            throw new InvalidOperationException("报告服务启动失败。\n记录：" + serverLog + "\n" + Tail(serverLog));
                    }
                    if (!started) throw new InvalidOperationException("报告服务尚未就绪。\n记录：" + serverLog);
                }
            }
            VerifyHealth(health, version, workspace, script, port);
            // Confirm that this exact report can be read before opening a browser.
            VerifyReport(serviceUrl);
            if (!noOpen)
            {
                Process.Start(new ProcessStartInfo(serviceUrl + "/Report.html") { UseShellExecute = true });
                WriteLog("Opened report in the default browser.");
            }
            WriteOutcome(new Dictionary<string, object> {
                { "status", "ready" }, { "started", started }, { "migrated", migrated }, { "browserOpened", !noOpen },
                { "workspace", workspace }, { "version", version }, { "port", port },
                { "pid", health["pid"] }, { "python", python }, { "serviceLog", serverLog },
                { "launcherSubsystem", "Windows GUI" }, { "childCreateNoWindow", true },
                { "reportUrl", serviceUrl + "/Report.html" }
            });
            return 0;
        }
        catch (Exception error)
        {
            WriteLog(error.ToString());
            WriteOutcome(new Dictionary<string, object> { { "status", "error" }, { "error", error.Message } });
            if (!noOpen)
                MessageBox.Show(error.Message, "Report", MessageBoxButtons.OK, MessageBoxIcon.Error);
            return 1;
        }
        finally
        {
            if (ownsMutex && launchMutex != null) launchMutex.ReleaseMutex();
            if (launchMutex != null) launchMutex.Dispose();
        }
    }

    private static string FindWorkspace(string initial)
    {
        DirectoryInfo directory = new DirectoryInfo(initial);
        while (directory != null)
        {
            string server = Path.Combine(directory.FullName, ProjectRelative, "runtime", "report_server.py");
            if (File.Exists(Path.Combine(directory.FullName, "Report.html")) && File.Exists(server))
                return directory.FullName.TrimEnd(Path.DirectorySeparatorChar);
            directory = directory.Parent;
        }
        throw new InvalidOperationException("找不到 Report.html 和报告运行环境。请把 Report.exe 放在现有报告目录中。");
    }

    private static string ExpectedVersion(string script)
    {
        Match match = Regex.Match(File.ReadAllText(script, Encoding.UTF8), "^VERSION\\s*=\\s*\"([^\"]+)\"", RegexOptions.Multiline);
        if (!match.Success) throw new InvalidOperationException("无法确认报告服务版本。");
        return match.Groups[1].Value;
    }

    private static string FindPython()
    {
        string programs = Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.LocalApplicationData), "Programs", "Python");
        List<string> candidates = new List<string>();
        candidates.Add(Path.Combine(programs, "Python313", "python.exe"));
        if (Directory.Exists(programs))
        {
            string[] installations = Directory.GetDirectories(programs, "Python*");
            Array.Sort(installations, StringComparer.OrdinalIgnoreCase);
            Array.Reverse(installations);
            foreach (string installation in installations) candidates.Add(Path.Combine(installation, "python.exe"));
        }
        foreach (string directory in (Environment.GetEnvironmentVariable("PATH") ?? "").Split(Path.PathSeparator))
        {
            if (!String.IsNullOrWhiteSpace(directory) && directory.IndexOf("WindowsApps", StringComparison.OrdinalIgnoreCase) < 0)
            {
                try { candidates.Add(Path.Combine(directory.Trim('"'), "python.exe")); }
                catch (ArgumentException) { }
            }
        }
        foreach (string candidate in candidates)
            if (File.Exists(candidate)) return Path.GetFullPath(candidate);
        throw new InvalidOperationException("现有 Python 环境不可用。请保留本机报告运行环境。");
    }

    private static Dictionary<string, object> Health(string serviceUrl)
    {
        try
        {
            using (HttpWebResponse response = (HttpWebResponse)Request(serviceUrl + "/api/health").GetResponse())
            using (StreamReader reader = new StreamReader(response.GetResponseStream(), Encoding.UTF8))
                return Json.Deserialize<Dictionary<string, object>>(reader.ReadToEnd());
        }
        catch (WebException) { return null; }
        catch (ArgumentException) { return null; }
        catch (InvalidOperationException) { return null; }
    }

    private static HttpWebRequest Request(string url)
    {
        HttpWebRequest request = (HttpWebRequest)WebRequest.Create(url);
        request.Proxy = null;
        request.Timeout = 1200;
        request.ReadWriteTimeout = 1200;
        request.KeepAlive = false;
        return request;
    }

    private static void VerifyHealth(Dictionary<string, object> health, string version, string workspace, string script, int port)
    {
        if (health == null || StringValue(health, "service") != ServiceName || StringValue(health, "version") != version)
            throw new InvalidOperationException("端口 " + port + " 上已有其他版本的报告服务，请先关闭旧报告后再打开。\n期望版本：" + version);
        if (StringValue(health, "status") != "ready")
            throw new InvalidOperationException("报告服务正在关闭，请稍后重新打开。");
        if (health.ContainsKey("workspace") && !SamePath(StringValue(health, "workspace"), workspace))
            throw new InvalidOperationException("报告端口正在服务另一个工作目录。");
        if (health.ContainsKey("script") && !SamePath(StringValue(health, "script"), script))
            throw new InvalidOperationException("报告服务路径与当前报告不一致。");
    }

    private static void MigrateIdleService(Dictionary<string, object> health, string workspace, string script, string serviceUrl, int port)
    {
        // Migration never force-kills a service and never interrupts an active
        // proof/cell. Unknown older protocols are deliberately not stopped.
        if (!health.ContainsKey("workspace") || !health.ContainsKey("script") || !health.ContainsKey("activeJobs") ||
            !SamePath(StringValue(health, "workspace"), workspace) || !SamePath(StringValue(health, "script"), script))
            throw new InvalidOperationException("已有旧版报告服务；无法确认它是否仍在计算，已保留该服务。请完成当前运行后重新打开。\n旧版本：" + StringValue(health, "version"));
        if (Convert.ToInt32(health["activeJobs"], CultureInfo.InvariantCulture) != 0)
            throw new InvalidOperationException("旧版报告仍在计算。请等待当前运行完成后重新打开报告。");
        string stateName = port == 8766 ? "server-state.json" : "server-state-" + port.ToString(CultureInfo.InvariantCulture) + ".json";
        string statePath = Path.Combine(Path.GetDirectoryName(script), stateName);
        if (!File.Exists(statePath)) throw new InvalidOperationException("无法确认旧版报告的运行状态，已保留该服务。");
        Dictionary<string, object> state = Json.Deserialize<Dictionary<string, object>>(File.ReadAllText(statePath, Encoding.UTF8));
        if (state == null || StringValue(state, "service") != ServiceName ||
            StringValue(state, "pid") != StringValue(health, "pid") || StringValue(state, "version") != StringValue(health, "version") ||
            StringValue(state, "port") != port.ToString(CultureInfo.InvariantCulture) ||
            !state.ContainsKey("workspace") || !state.ContainsKey("script") ||
            !SamePath(StringValue(state, "workspace"), workspace) || !SamePath(StringValue(state, "script"), script) ||
            StringValue(state, "token").Length < 16)
            throw new InvalidOperationException("旧版报告服务与当前目录的运行状态不一致，已保留该服务。");
        byte[] body = Encoding.UTF8.GetBytes(Json.Serialize(new Dictionary<string, object> {
            { "token", StringValue(state, "token") }, { "idleOnly", true }
        }));
        HttpWebRequest request = Request(serviceUrl + "/api/stop");
        request.Method = "POST";
        request.ContentType = "application/json";
        request.Headers["Origin"] = serviceUrl;
        request.ContentLength = body.Length;
        try
        {
            using (Stream upload = request.GetRequestStream()) upload.Write(body, 0, body.Length);
            using (HttpWebResponse response = (HttpWebResponse)request.GetResponse())
            using (StreamReader reader = new StreamReader(response.GetResponseStream(), Encoding.UTF8))
            {
                if (response.StatusCode != HttpStatusCode.OK)
                    throw new InvalidOperationException("旧版报告未接受安全换版，已保留该服务。");
                reader.ReadToEnd();
            }
        }
        catch (WebException error)
        {
            HttpWebResponse failed = error.Response as HttpWebResponse;
            if (failed != null && failed.StatusCode == HttpStatusCode.Conflict)
                throw new InvalidOperationException("旧版报告仍在计算。请等待当前运行完成后重新打开报告。");
            throw new InvalidOperationException("旧版报告未接受安全换版，已保留该服务。请完成当前运行后重新打开。");
        }
        WriteLog("Safely stopping idle prior version " + StringValue(health, "version") + " PID " + StringValue(health, "pid"));
        Stopwatch timer = Stopwatch.StartNew();
        while (timer.Elapsed < TimeSpan.FromSeconds(45))
        {
            Thread.Sleep(250);
            if (!PortOpen(port)) return;
        }
        throw new InvalidOperationException("旧版报告正在退出，请稍后重新打开。");
    }

    private static bool SamePath(string left, string right)
    {
        return String.Equals(Path.GetFullPath(left).TrimEnd(Path.DirectorySeparatorChar), Path.GetFullPath(right).TrimEnd(Path.DirectorySeparatorChar), StringComparison.OrdinalIgnoreCase);
    }

    private static void VerifyReport(string serviceUrl)
    {
        using (HttpWebResponse response = (HttpWebResponse)Request(serviceUrl + "/Report.html").GetResponse())
        {
            if (response.StatusCode != HttpStatusCode.OK || !response.ContentType.StartsWith("text/html", StringComparison.OrdinalIgnoreCase))
                throw new InvalidOperationException("报告页面暂时不可用。");
            using (StreamReader reader = new StreamReader(response.GetResponseStream(), Encoding.UTF8))
            {
                string html = reader.ReadToEnd();
                string prefix = html.Substring(0, Math.Min(html.Length, 4096));
                if (prefix.IndexOf("<html", StringComparison.OrdinalIgnoreCase) < 0)
                    throw new InvalidOperationException("报告页面内容无效。");
            }
        }
    }

    private static bool PortOpen(int port)
    {
        try
        {
            using (TcpClient client = new TcpClient())
            {
                IAsyncResult pending = client.BeginConnect("127.0.0.1", port, null, null);
                if (!pending.AsyncWaitHandle.WaitOne(300)) return false;
                client.EndConnect(pending);
                return true;
            }
        }
        catch (SocketException) { return false; }
    }

    // Windows CommandLineToArgvW-compatible quoting, including embedded newlines.
    private static string Quote(string value)
    {
        StringBuilder quoted = new StringBuilder("\"");
        int slashes = 0;
        foreach (char character in value)
        {
            if (character == '\\') { slashes++; continue; }
            if (character == '"')
            {
                quoted.Append('\\', slashes * 2 + 1);
                quoted.Append(character);
            }
            else
            {
                quoted.Append('\\', slashes);
                quoted.Append(character);
            }
            slashes = 0;
        }
        quoted.Append('\\', slashes * 2);
        quoted.Append('"');
        return quoted.ToString();
    }

    private static string Digest(string text)
    {
        using (SHA256 hash = SHA256.Create())
            return BitConverter.ToString(hash.ComputeHash(Encoding.UTF8.GetBytes(text))).Replace("-", "").Substring(0, 24);
    }

    private static string StringValue(Dictionary<string, object> value, string key)
    {
        object result;
        return value.TryGetValue(key, out result) && result != null ? Convert.ToString(result, CultureInfo.InvariantCulture) : "";
    }

    private static string Tail(string path)
    {
        try
        {
            using (FileStream file = new FileStream(path, FileMode.Open, FileAccess.Read, FileShare.ReadWrite))
            using (StreamReader reader = new StreamReader(file, Encoding.UTF8))
            {
                string text = reader.ReadToEnd();
                return text.Length > 1200 ? text.Substring(text.Length - 1200) : text;
            }
        }
        catch (IOException) { return ""; }
    }

    private static void WriteLog(string message)
    {
        if (logPath == null) return;
        try { File.AppendAllText(logPath, DateTime.UtcNow.ToString("o", CultureInfo.InvariantCulture) + " " + message + Environment.NewLine, Encoding.UTF8); }
        catch (IOException) { }
    }

    private static void WriteOutcome(Dictionary<string, object> value)
    {
        if (outcomePath == null) return;
        value["utc"] = DateTime.UtcNow.ToString("o", CultureInfo.InvariantCulture);
        try { File.WriteAllText(outcomePath, Json.Serialize(value) + Environment.NewLine, Encoding.UTF8); }
        catch (IOException) { }
    }
}
