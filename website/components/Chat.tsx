const Chat = ({msg}:{msg:String;}) => {
  return (
    <div className="p-2 max-w-96 rounded-lg bg-sky-600 my-1">
        {msg}
    </div>
  )
}

export default Chat