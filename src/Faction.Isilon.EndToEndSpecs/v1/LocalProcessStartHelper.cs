using System.Diagnostics;
using System.IO;

namespace Faction.Isilon.EndToEndSpecs.v1
{
    public static class LocalProcessStartHelper
    {
        public static void run_cmd_in_shell(string fileName, string cmd, string args)
        {
            ProcessStartInfo start = new ProcessStartInfo();
            start.FileName = fileName;
            start.Arguments = $"\"{cmd}\" \"{args}\"";
            start.UseShellExecute = true;
            start.CreateNoWindow = true; 
            start.RedirectStandardOutput = false;
            start.RedirectStandardError = false;
            Process.Start(start);
        }
        
        public static string run_cmd(string fileName, string cmd, string args)
        {
            ProcessStartInfo start = new ProcessStartInfo();
            start.FileName = fileName;
            start.Arguments = $"\"{cmd}\" \"{args}\"";
            start.UseShellExecute = false;
            start.CreateNoWindow = true; 
            start.RedirectStandardOutput = true;
            start.RedirectStandardError = true;
            Process.Start(start);
            
            using (Process process = Process.Start(start))
            {
                using (StreamReader reader = process?.StandardOutput)
                {
                    string stderr = process?.StandardError.ReadToEnd();
                    string result = reader?.ReadToEnd(); 
                    return result;
                }
            }
        }
    }
}
