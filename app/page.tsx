'use client'; // Required for client-side code

import React, { useState } from 'react';

export default function Home() {
  const [file, setFile] = useState<File | null>(null);

  // Handle file input change
  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      setFile(e.target.files[0]);
    }
  };

  // Handle form submission
  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    if (!file) {
      alert('Please select a file first');
      return;
    }

    const formData = new FormData();
    formData.append('file', file); // Ensure the field name is 'file'

    try {
      // Fetch request to the Flask backend
      const res = await fetch('http://127.0.0.1:5000/predict', {
        method: 'POST',
        body: formData, // Assuming you have a FormData object containing the file
      });
  
      // Check if the response is okay
      if (res.ok) {
        // Handle the response as a PDF file
        const blob = await res.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'tumor_report.pdf'; // Filename for the downloaded PDF
        a.click();
        window.URL.revokeObjectURL(url); // Clean up the object URL
      } else {
        // Handle unsuccessful response
        const errorData = await res.json(); // Assuming the backend returns JSON with error details
        alert(`Upload failed: ${errorData.message || 'Unknown error'}`);
      }
    } catch (error) {
      // Handle any errors during the fetch request
      console.error('Error:', error);
      alert('An error occurred');
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-r from-blue-400 to-green-400 flex flex-col items-center justify-center p-4">
      <h1 className="text-5xl font-bold text-white mb-10">MRI Tumor Analysis</h1>

      <form onSubmit={handleSubmit} className="bg-white p-6 sm:p-4 rounded-lg shadow-lg w-full max-w-md md:max-w-lg lg:max-w-xl">
        {/* File Upload Input */}
        <label className="block mb-4 text-sm font-medium text-gray-700">
          Upload MRI Image:
        </label>
        <input
          type="file"
          accept="image/jpeg, image/png"
          onChange={handleFileChange}
          className="block w-full text-sm text-gray-900 border border-gray-300 rounded-lg cursor-pointer bg-gray-50 focus:outline-none focus:border-blue-500"
        />

        {/* Submit Button */}
        <button
          type="submit"
          className="mt-4 w-full py-2 px-4 bg-blue-600 text-white rounded hover:bg-blue-700 transition-all"
        >
          Analyze Image
        </button>
      </form>
    </div>
  );
}
