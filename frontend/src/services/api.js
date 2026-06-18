const BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:5000/api";

export async function screenResumes(jobTitle, jobDescription, files) {
  const formData = new FormData();
  formData.append("job_title", jobTitle);
  formData.append("job_description", jobDescription);
  files.forEach((file) => formData.append("resumes", file));

  const response = await fetch(`${BASE_URL}/screen`, {
    method: "POST",
    body: formData,
  });

  if (!response.ok) {
    const err = await response.json().catch(() => ({}));
    throw new Error(err.error || `Server error: ${response.status}`);
  }

  return response.json();
}

export async function fetchSampleJD() {
  const response = await fetch(`${BASE_URL}/sample-jd`);
  if (!response.ok) throw new Error("Failed to fetch sample JD");
  return response.json();
}

export async function healthCheck() {
  const response = await fetch(`${BASE_URL}/health`);
  return response.ok;
}