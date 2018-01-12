using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;

namespace DLLAsynch2
{
    public class PiMessage
    {
        public void ProcessMessage(object sender, MessageEventArgs msg)
        {
            string LogMessage = String.Format("From ProcessMessage Read {0} bytes from socket. \n Data : {1}",
                      msg.Message.Length, msg.Message);

            //extract message counter and stop after 5,000 messages

            AsynchronousSocketListener SObject = (AsynchronousSocketListener)sender;
            if ( SObject.MessageRecv > 10 )
            {
                SObject.Response = "QT";
            }
               

            WriteToLogFile(LogMessage);
        }

        private void WriteToLogFile(string LogMessage)
        {
            using (System.IO.StreamWriter logfile = File.AppendText(@"C:\logs\windows.txt"))
            {
                logfile.WriteLine(LogMessage);
            }
        }
    }
}
