import { api } from "../api";

export default function Apply() {
  const submit = async (e) => {
    e.preventDefault();
    const formData = new FormData();
    [...e.target.documents.files].forEach((f) =>
      formData.append("documents", f)
    );
    try {
      await api.post("/applications", formData);
      alert("Application submitted successfully");
    } catch (err) {
      alert("Error submitting application");
    }
  };

  return (
    <form onSubmit={submit}>
      <h2>Apply for Study Loan</h2>
      <input type="file" name="documents" multiple required />
      <button>Submit</button>
    </form>
  );
}
