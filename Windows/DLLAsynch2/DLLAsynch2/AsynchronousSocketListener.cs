using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Net;
using System.Net.Sockets;
using System.Text;
using System.Threading;
using UnityEngine;
namespace DLLAsynch2
{
    public delegate void MessageArrivedEventHandler(object sender, MessageEventArgs e);
    public class AsynchronousSocketListener
    {

        public event MessageArrivedEventHandler MessageCompleted;

        // Thread signal.  
        public static ManualResetEvent allDone = new ManualResetEvent(false);

        public AsynchronousSocketListener(MessageArrivedEventHandler handler)
        {
            MessageCompleted = handler;
        }
        long _messageRecv = 0;

        Boolean listenForMsgs = true;

        public long MessageRecv
        {
            get
            {
                return _messageRecv;
            }
        }
        private string _response ="OK";  // Backing store

        public string Response
        {
            get
            {
                return _response;
            }
            set
            {
                _response = value;
            }
        }




        private void OnMessageComplete(MessageEventArgs e)
        {
            _messageRecv++;
            if (MessageCompleted != null)
            {
                MessageCompleted(this, e);
            }
        }

        public void SetupThread()
        {
            WriteToLogFile("Thread started");
            ThreadStart work = StartListening;
            Thread thread = new Thread(work);
            thread.Start();
            WriteToLogFile("Thread started");
        }
        public void StartListening()
        {
            // Data buffer for incoming data.  
            Byte[] bytes = new Byte[1024];

            // Establish the local endpoint for the socket.  
            // The DNS name of the computer  
            // running the listener is "host.contoso.com".  
            IPHostEntry ipHostInfo = Dns.GetHostEntry(Dns.GetHostName());
            //IPAddress ipAddress = ipHostInfo.AddressList[3];
            IPAddress ipAddress = IPAddress.Parse("192.168.1.24");
            EndPoint localEndPoint = new IPEndPoint(ipAddress, 11000);

            // Create a TCP/IP socket.  
            //Socket listener = new Socket(AddressFamily.InterNetwork,
            //    SocketType.Stream, ProtocolType.Tcp);

            Socket listener = new Socket(ipAddress.AddressFamily, SocketType.Stream, ProtocolType.Tcp);


            // Bind the socket to the local endpoint and listen for incoming connections.  
            try
            {
                listener.Bind(localEndPoint);
                listener.Listen(100);

                while (listenForMsgs)
                {
                    // Start an asynchronous socket to listen for connections. 
                    allDone.Reset();
                    listener.BeginAccept(
                        new AsyncCallback(AcceptCallback),
                        listener);

                    // Wait until a connection is made before continuing.  
                    allDone.WaitOne();
                }

            }
            catch (Exception e)
            {
                Console.WriteLine(e.ToString());
            }

            //Console.WriteLine("\nPress ENTER to continue...");
            //Console.Read();

        }

        public void AcceptCallback(IAsyncResult ar)
        {
            // Signal the main thread to continue.  
            WriteToLogFile("AcceptCallBack");


            // Get the socket that handles the client request.  
            Socket listener = (Socket)ar.AsyncState;
            Socket handler = listener.EndAccept(ar);

            // Create the state object.  
            while (listenForMsgs)
            {
                WriteToLogFile("Wait for Messages");
                allDone.Set();
                StateObject state = new StateObject();
                state.workSocket = handler;
                handler.BeginReceive(state.buffer, 0, StateObject.BufferSize, 0,
                    new AsyncCallback(ReadCallback), state);
                allDone.WaitOne();
            }

        }

        public void ReadCallback(IAsyncResult ar)
        {
            String content = String.Empty;

            // Retrieve the state object and the handler socket  
            // from the asynchronous state object.  
            StateObject state = (StateObject)ar.AsyncState;
            Socket handler = state.workSocket;

            // Read data from the client socket.   
            int bytesRead = handler.EndReceive(ar);
            //int bytesRead = handler.Receive(state.buffer);
            WriteToLogFile(string.Format("BytesRead {0}", bytesRead));
            if (bytesRead > 0)
            {
                // There  might be more data, so store the data received so far.  
                state.sb.Append(Encoding.ASCII.GetString(
                    state.buffer, 0, bytesRead));

                // Check for end-of-file tag. If it is not there, read   
                // more data.  
                content = state.sb.ToString();
                if (content.IndexOf("<EOF>") > -1)
                {
                    // All the data has been read from the   
                    // client. Display it on the console.  
                    WriteToLogFile( String.Format("Read {0} bytes from socket. \n Data : {1}",
                        content.Length, content));
                    WriteToLogFile("Message seen");
                    MessageEventArgs msgEvent = new MessageEventArgs(content);
                    OnMessageComplete(msgEvent);
                    //Raise event
                    // Echo the data back to the client.  
                    Send(handler, content);
                }
                else
                {
                    // Not all data received. Get more.  
                    handler.BeginReceive(state.buffer, 0, StateObject.BufferSize, 0,
                    new AsyncCallback(ReadCallback), state);
                }
            }
        }

        private void Send(Socket handler, String data)
        {
            // Convert the string data to byte data using ASCII encoding.  
            byte[] byteData = Encoding.ASCII.GetBytes(Response);

            // Begin sending the data to the remote device.  
            handler.BeginSend(byteData, 0, byteData.Length, 0,
                new AsyncCallback(SendCallback), handler);
        }

        private void SendCallback(IAsyncResult ar)
        {
            try
            {
                // Retrieve the socket from the state object.  
                Socket handler = (Socket)ar.AsyncState;

                // Complete sending the data to the remote device.  
                int bytesSent = handler.EndSend(ar);
                string LogMsg = string.Format ("Sent {0} bytes to client.", bytesSent);
                if ( Response == "QT")
                {
                    listenForMsgs = false;
                }
                WriteToLogFile(LogMsg);
                allDone.Set();

                //handler.Shutdown(SocketShutdown.Both);
                //handler.Close();

            }
            catch (Exception e)
            {
                Console.WriteLine(e.ToString());
            }
        }

        private void WriteToLogFile(string LogMessage)
        {
            Console.WriteLine(LogMessage);
            //using (System.IO.StreamWriter logfile = File.AppendText(@"C:\logs\SendRecv.txt"))
            //{
            //    logfile.WriteLine(LogMessage);
            //}
        }
    }
}
