## PhoneIT

An application that when deployed can establish a call service, where an AI agent can solve any query of the users using an established RAG pipeline. The system is centralized using a web platform for ease of use and monitoring for the service hoster.

## Features

- Utilizes various open-source models like [indictrans2](https://huggingface.co/ai4bharat/indictrans2-en-indic-dist-200M) for multi-lingual efficiency and performance.
- Contains an efficient RAG pipeline ensuring the AI provides factual information via a vector DB(FAISS).
- Integrated with Twilio API.
- Currently the cheapest option in the market as of its creation time.

## Installation

### Running Only the Application

1. Create a Python virtual environment (version <= 3.10).
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Update the required details in the `.env` file present in the same directory.
4. Run the application:
   ```bash
   python final.py
   ```

### Running with Web Interface

1. Install Node.js and npm.
2. Navigate to the web interface directory:
   ```bash
   cd website
   ```
3. Install dependencies:
   ```bash
   npm install
   ```
4. Run the development server:
   ```bash
   npm run dev
   ```
5. Open [http://localhost:3000](http://localhost:3000) in your browser to see the result.

## Contributing

This project was developed within 1-2 days. Hence, any kind of suggestions and upgrades are appreciated 🙂.

## License

This project is licensed under the Apache 2.0 License.
