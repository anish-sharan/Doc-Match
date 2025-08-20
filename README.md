# DocMatch

DocMatch is a web application that automates the verification of purchase orders (PO) and invoices using OCR and an LLM (Large Language Model). It extracts text from uploaded documents, compares them intelligently, and provides a clear match/mismatch report.

## Features

- Upload multiple PO and invoice files at once.
- OCR-based text extraction from PDFs.
- Intelligent comparison using an LLM.
- Visual match/mismatch results with JSON details.
- User-friendly interface with file preview and deletion.

## Workflow

1. **Upload Files** – Select multiple PO and invoice PDFs.  
2. **OCR Extraction** – Extract text from each document.  
3. **LLM Comparison** – Compare PO and invoice data using a language model.  
4. **Result Display** – Show match/mismatch status with detailed JSON output.  

## Tech Stack

- **Frontend:** React, TypeScript, Axios, CSS  
- **Backend:** FastAPI, Python  
- **AI:** OCR service + LLM for intelligent comparison  

## Installation

1. Clone the repository:

```bash
git clone <repo-url>
cd <repo-folder>