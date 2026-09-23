import axios from "axios";


const api = axios.create({
    baseURL: import.meta.env.VITE_API_URL
});


export async function uploadPDF(file) {

    const formData = new FormData();

    formData.append("file", file);

    const response = await api.post(
        "/documents/upload",
        formData
    );

    return response.data;
}


export async function askQuestion(question, sessionId) {

    const response = await api.post(
        "/chat/",
        {
            question: question,
            session_id: sessionId
        }
    );

    return response.data;
}