using DLLAsynch2;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace ConsoleApp1
{
    class Program
    {
        static void Main(string[] args)
        {

            Console.WriteLine("Start");
            PiMessage msgProc = new PiMessage();

            MessageArrivedEventHandler allProc = msgProc.ProcessMessage;

            AsynchronousSocketListener listen = new AsynchronousSocketListener(allProc);

            listen.StartListening();
            //listen.SetupThread();
            Console.WriteLine("Done");
        }
    }
}
