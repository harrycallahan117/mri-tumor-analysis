This is a [Next.js](https://nextjs.org) project bootstrapped with [`create-next-app`](https://nextjs.org/docs/app/api-reference/cli/create-next-app).

# MRI Tumor Classification API

This project is a full-stack web application that allows users to upload MRI scans and receive a PDF report classifying the scan into one of four categories: Glioma Tumor, Meningioma Tumor, Normal, or Pituitary Tumor.

The backend uses a pre-trained TensorFlow model served through a Flask API, while the frontend allows users to upload images and receive classification reports.

## Model Performance

- **Training Accuracy**: 98.75%
- **Testing Accuracy**: 90%
- We are continuously working on improving the model to achieve better generalization and real-world performance.

## Features

- **Upload MRI scans**: Users can upload images in `.png`, `.jpg`, or `.jpeg` formats.
- **Automated classification**: The API classifies the scan into one of the four categories.
- **PDF report generation**: The results are provided in a downloadable PDF format.

## Installation

### Clone the repository

```bash
git clone https://github.com/yourusername/yourprojectname.git
cd yourprojectname


## Getting Started

First, run the development server:

```bash
npm run dev
# or
yarn dev
# or
pnpm dev
# or
bun dev
```

Open [http://localhost:3000](http://localhost:3000) with your browser to see the result.

You can start editing the page by modifying `app/page.tsx`. The page auto-updates as you edit the file.

This project uses [`next/font`](https://nextjs.org/docs/app/building-your-application/optimizing/fonts) to automatically optimize and load [Geist](https://vercel.com/font), a new font family for Vercel.

## Learn More

To learn more about Next.js, take a look at the following resources:

- [Next.js Documentation](https://nextjs.org/docs) - learn about Next.js features and API.
- [Learn Next.js](https://nextjs.org/learn) - an interactive Next.js tutorial.

You can check out [the Next.js GitHub repository](https://github.com/vercel/next.js) - your feedback and contributions are welcome!

