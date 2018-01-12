using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace DLLAsynch2
{
    public class MessageEventArgs : EventArgs
    {
        private string m_Message = string.Empty;

        public MessageEventArgs(string arrived)
        {
            m_Message = arrived;
        }

        public string Message
        {
            get { return m_Message; }
        }
    }
}
