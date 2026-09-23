import { useRef, useState } from "react";

import { uploadPDF, askQuestion } from "./api";

import "./App.css";


function App() {

    const [file, setFile] = useState(null);
    const [sessionId, setSessionId] = useState("");
    const [messages, setMessages] = useState([]);
    const [question, setQuestion] = useState("");

    const [uploading, setUploading] = useState(false);
    const [chatting, setChatting] = useState(false);

    const fileInputRef = useRef(null);


    function handlePlusClick() {
        fileInputRef.current.click();
    }


    async function handleFileChange(event) {

        const selectedFile = event.target.files[0];

        if (!selectedFile) {
            return;
        }


        if (selectedFile.type !== "application/pdf") {

            setMessages([
                {
                    role: "assistant",
                    content: "Please upload a PDF file."
                }
            ]);

            return;
        }


        try {

            setUploading(true);


            const data = await uploadPDF(selectedFile);


            setFile(selectedFile);

            setSessionId(data.session_id);


            setMessages([
                {
                    role: "assistant",
                    content:
                        `I've loaded "${selectedFile.name}". ` +
                        `It contains ${data.chunks} chunks. ` +
                        `You can now ask questions about it.`
                }
            ]);


        } catch (error) {

            console.error(error);

            setMessages([
                {
                    role: "assistant",
                    content:
                        "I couldn't upload that PDF. Please try again."
                }
            ]);

        } finally {

            setUploading(false);

        }


        event.target.value = "";
    }


    async function handleSend() {

        const trimmedQuestion = question.trim();


        if (!trimmedQuestion) {
            return;
        }


        if (!sessionId) {

            setMessages((previous) => [
                ...previous,
                {
                    role: "assistant",
                    content:
                        "Please upload a PDF first using the + button."
                }
            ]);

            return;
        }


        setMessages((previous) => [
            ...previous,
            {
                role: "user",
                content: trimmedQuestion
            }
        ]);


        setQuestion("");
        setChatting(true);


        try {

            const data = await askQuestion(
                trimmedQuestion,
                sessionId
            );


            setMessages((previous) => [
                ...previous,
                {
                    role: "assistant",
                    content: data.answer,
                    sources: data.sources || []
                }
            ]);


        } catch (error) {

            console.error(error);


            setMessages((previous) => [
                ...previous,
                {
                    role: "assistant",
                    content:
                        "Something went wrong while answering your question."
                }
            ]);

        } finally {

            setChatting(false);

        }
    }


    function handleKeyDown(event) {

        if (
            event.key === "Enter" &&
            !event.shiftKey
        ) {

            event.preventDefault();

            handleSend();
        }
    }


    return (
        <div className="app">

            <div className="chat-container">


                {/* Header */}

                <header className="header">

                    <div>

                        <h1>
                            AI Support Agent
                        </h1>

                        <p>
                            Chat with your PDF
                        </p>

                    </div>


                    {file && (

                        <div className="file-badge">

                            📄 {file.name}

                        </div>

                    )}

                </header>


                {/* Messages */}

                <main className="messages">


                    {messages.length === 0 && (

                        <div className="welcome">

                            <h2>
                                Upload a PDF to get started
                            </h2>

                            <p>
                                Ask questions and get answers
                                based only on your document.
                            </p>

                            <button
                                className="upload-start-button"
                                onClick={handlePlusClick}
                            >
                                + Upload PDF
                            </button>

                        </div>

                    )}


                    {messages.map((message, index) => (

                        <div
                            key={index}
                            className={`message-row ${message.role}`}
                        >

                            <div className="message">

                                {message.content}


                                {message.sources &&
                                    message.sources.length > 0 && (

                                        <div className="sources">

                                            <strong>
                                                Sources
                                            </strong>


                                            {message.sources.map(
                                                (source, sourceIndex) => {

                                                    return (
                                                        <div
                                                            key={sourceIndex}
                                                            className="source"
                                                        >
                                                            📄 {source.filename}
                                                            {" — "}
                                                            Page {source.page}
                                                        </div>
                                                    );

                                                }
                                            )}

                                        </div>

                                    )}

                            </div>

                        </div>

                    ))}


                    {uploading && (

                        <div className="message-row assistant">

                            <div className="message">
                                Uploading and processing your PDF...
                            </div>

                        </div>

                    )}


                    {chatting && (

                        <div className="message-row assistant">

                            <div className="message">
                                Thinking...
                            </div>

                        </div>

                    )}

                </main>


                {/* Hidden PDF input */}

                <input
                    ref={fileInputRef}
                    type="file"
                    accept=".pdf,application/pdf"
                    onChange={handleFileChange}
                    hidden
                />


                {/* Chat input */}

                <div className="input-area">

                    <button
                        className="plus-button"
                        onClick={handlePlusClick}
                        disabled={uploading}
                        title="Upload PDF"
                    >
                        +
                    </button>


                    <textarea
                        value={question}
                        onChange={(event) => {
                            setQuestion(event.target.value);
                        }}
                        onKeyDown={handleKeyDown}
                        placeholder={
                            sessionId
                                ? "Ask anything about your PDF..."
                                : "Upload a PDF first..."
                        }
                        disabled={
                            !sessionId ||
                            chatting ||
                            uploading
                        }
                        rows={1}
                    />


                    <button
                        className="send-button"
                        onClick={handleSend}
                        disabled={
                            !question.trim() ||
                            !sessionId ||
                            chatting ||
                            uploading
                        }
                    >
                        ↑
                    </button>

                </div>


                <p className="footer-text">
                    AI Support Agent can only answer from your uploaded document.
                </p>

            </div>

        </div>
    );
}


export default App;