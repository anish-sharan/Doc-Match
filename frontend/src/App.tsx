import { useState } from "react";
import axios from "axios";
import "./App.css";

interface UploadedFile {
  file: File;
  name: string;
  size: number;
}

interface ComparisonResult {
  po_file: string;
  invoice_file: string;
  comparison_result: string;
  comparison_result_json: any;
}

const App: React.FC = () => {
  const [files, setFiles] = useState<UploadedFile[]>([]);
  const [results, setResults] = useState<ComparisonResult[]>([]);
  const [loading, setLoading] = useState(false);

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFiles = event.target.files;
    if (selectedFiles) {
      const newFiles: UploadedFile[] = Array.from(selectedFiles).map(
        (file) => ({
          file,
          name: file.name,
          size: file.size,
        })
      );
      setFiles((prevFiles) => [...prevFiles, ...newFiles]);
    }
    event.target.value = "";
  };

  const handleDeleteFile = (index: number) => {
    setFiles((prevFiles) => prevFiles.filter((_, i) => i !== index));
  };

  const handleUpload = async () => {
    if (files.length === 0) return alert("Please select files to upload.");

    const formData = new FormData();
    files.forEach((f) => formData.append("files", f.file));

    try {
      setLoading(true);
      const response = await axios.post(
        "http://127.0.0.1:8000/api/upload",
        formData,
        {
          headers: { "Content-Type": "multipart/form-data" },
        }
      );
      setResults(response.data.results || []);
    } catch (error: any) {
      console.error("Upload failed:", error);
      alert("Upload failed. Check console for details.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app-container">
      <h1 className="app-title">Multi File Upload App</h1>

      <div className="file-input-container">
        <label htmlFor="fileInput" className="file-input-label">
          Select PO/Invoice Files
        </label>
        <input
          type="file"
          id="fileInput"
          multiple
          onChange={handleFileChange}
          className="file-input"
        />
      </div>

      {files.length > 0 && (
        <div className="files-list-container">
          <h2 className="section-title">Selected Files</h2>
          <ul className="files-list">
            {files.map((file, index) => (
              <li key={index} className="file-item">
                <div>
                  <span className="file-name">{file.name}</span>
                  <span className="file-size">
                    {(file.size / 1024).toFixed(2)} KB
                  </span>
                </div>
                <button
                  className="delete-button"
                  onClick={() => handleDeleteFile(index)}
                >
                  ✕
                </button>
              </li>
            ))}
          </ul>
          <button
            className="upload-button"
            onClick={handleUpload}
            disabled={loading}
          >
            {loading ? "Uploading..." : "Upload All Files"}
          </button>
        </div>
      )}

      {results.length > 0 && (
        <div className="results-container">
          <h2 className="section-title">Comparison Results</h2>
          {results.map((res, idx) => {
            console.log(res);
            const isMatch = res.comparison_result_json.status == 'match';
            return (
              <div key={idx} className="result-item">
                <p className="result-summary">
                  <strong>PO:</strong> {res.po_file} | <strong>Invoice:</strong>{" "}
                  {res.invoice_file} | <strong>Result:</strong>{" "}
                  <span className={isMatch ? "match" : "mismatch"}>
                    {isMatch ? "✔️ Match" : "❌ Mismatch"}
                  </span>
                </p>
                <pre className="result-json">
                  {JSON.stringify(res.comparison_result_json, null, 2)}
                </pre>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
};

export default App;
