const ResponseChat = ({ msg }: { msg: String }) => {
  return (
    <div className="flex w-full justify-end my-1">
      <div className="max-w-96 p-2 text-right rounded-lg bg-slate-800">
        {msg}
      </div>
    </div>
  );
};

export default ResponseChat;
