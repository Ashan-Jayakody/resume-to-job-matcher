import { useState } from "react";
import heroImage from "../assets/platform-image.png";

export default function ResumeToJob() {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [data, setData] = useState(null);
  const [error, setError] = useState("");

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!file) {
      setError("Please select a file");
      return;
    }

    setError("");
    setLoading(true);
    setData(null);
    try {
      const formData = new FormData();
      formData.append("file", file);

      const Backend_URL = "https://resume-to-job-matcher-52v9.onrender.com/";

      const res = await fetch(`${Backend_URL}/match`, {
        method: "POST",
        body: formData,
      });

      const json = await res.json();
      setData(json);
    } catch (err) {
      setError("Something went wrong");
    } finally {
      setLoading(false);
    }
  };
  return (
    <div className="bg-white flex-auto min-h-screen">
      <div>
        <div className="p-6 mt-16 mx-10 flex-col bg-white">
          <h1 className=" text-center font-mono text-4xl font-semibold text-black ">
            Resume-To-Job
          </h1>
          <h1 className=" text-center font-sans text-6xl font-bold bg-gradient-to-r from-blue-500 to-indigo-400 bg-clip-text text-transparent mt-4">
            Find Your Perfect Job Match
          </h1>
          <p className="text-center text-xl font-italic text-gray-400 pt-8">
            Upload your CV and get the best job opportunities that perfectly
            match your skills.{" "}
          </p>
        </div>

        <div className="flex justify-center px-6">
          <div className="w-full max-w-5xl rounded-2xl">
            <img
              src={heroImage}
              alt="job matching platform"
              className="w-full h-auto rounded-2xl shadow-card-hover object-cover"
            />
          </div>
        </div>

        <form
          onSubmit={handleSubmit}
          className="max-w-md h-50 mx-auto mt-20 m bg-sky-50 rounded-lg shadow p-6 space-y-4"
        >
          <h2 className="text-xl font-semibold text-gray-800 text-center">
            Upload Your CV
          </h2>

          <input
            type="file"
            accept=".pdf,.docx"
            onChange={handleFileChange}
            className="block w-full text-sm text-gray-700 border border-gray-300 rounded-md cursor-pointer focus:outline-none focus:ring-2 focus:ring-green-400 focus:border-blue-400"
          />

          <button
            type="submit"
            disabled={loading}
            className="w-full bg-blue-500 text-white py-2 rounded-md font-medium hover:bg-blue-500/80 disabled:opacity-50 transition"
          >
            {loading ? "Uploading..." : "Match Jobs"}
          </button>
        </form>

        <div className="max-w-5xl mx-auto mt-4 p-6 bg-gray-50 rounded-xl">
          {error && <p>{error}</p>}

          {data && (
            <div>
              <div className="bg-white rounded-xl shadow-sm p-6 border border-gray-100">
                <h2 className="text-2xl font-bold text-gray-900 mb-4 flex items-center gap-2">
                  {" "}
                  Your skills:
                </h2>

                <div className="flex gap-2">
                  {data.extracted_skills?.map((skill) => (
                    <span
                      key={skill}
                      className="items-center px-3 py-1 rounded-full text-sm font-medium bg-blue-100 text-blue-800 "
                    >
                      {skill}
                    </span>
                  ))}
                </div>
              </div>

              <div className="py-8">
                <h2 className="text-2xl font-bold text-gray-900 mb-6">
                  Matching jobs:
                </h2>
                {data.matches?.map((job, idx) => (
                  <div
                    key={idx}
                    className="bg-white rounded-xl shadow-sm p-6 border border-gray-100 my-8"
                  >
                    <h3 className="text-xl font-semibold text-gray-900 mb-2 leading-tight">
                      {job.title}
                    </h3>
                    <p className="flex gap-2 text-gray-600 mb-2">
                      Company:{" "}
                      <span className=" font-medium">{job.company}</span>
                    </p>
                    <p className="flex gap-2 text-gray-600 mb-2">
                      Location:{" "}
                      <span className=" font-medium">{job.location}</span>
                    </p>

                    <h4 className="text-sm font-semibold text-gray-700 mt-4 ">
                      Required Skills:
                    </h4>
                    <div className="flex gap-2 my-2">
                      {job.skills_required.map((skill) => (
                        <span
                          key={skill}
                          className="inline-flex items-center px-2 py-1 rounded text-sm font-medium bg-gray-100 text-gray-700 border border-gray-200"
                        >
                          {" "}
                          {skill}
                        </span>
                      ))}
                    </div>

                    <h4 className="text-sm font-semibold text-gray-700 mt-4  ">
                      Your Matching Skills:
                    </h4>
                    <div className="flex gap-2 my-2">
                      {job.matching_skills.map((skill) => (
                        <span
                          key={skill}
                          className="inline-flex items-center px-2 py-1 rounded text-sm font-medium bg-green-100 text-green-700 border border-gray-200"
                        >
                          {" "}
                          {skill}
                        </span>
                      ))}
                    </div>

                    <a
                      className="inline-flex items-center mt-4 w-full justify-center px-6 py-2 bg-blue-600 hover:bg-blue-700 text-white text-sm font-medium rounded-lg transition-colors duration-200"
                      href={job.link}
                      target="_blank"
                      rel="noopener noreferrer"
                    >
                      view job
                    </a>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>

      <footer className="border-t border-border bg-card/30 mt-20">
        <div className="container mx-auto px-4 py-8">
          <div className="text-center text-muted-foreground">
            <p>
              &copy; 2025 JobMatcher. Find your perfect career
              match.
            </p>
          </div>
        </div>
      </footer>
    </div>
  );
}
