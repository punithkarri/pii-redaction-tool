# Scaler AI Labs — PII Redaction Tool Submission Links

### 1. Repository & Deployment Links
* **GitHub Repository**: [https://github.com/punithkarri/pii-redaction-tool](https://github.com/punithkarri/pii-redaction-tool)
* **Vercel Production Site**: *[To be generated upon running deployment below]*
* **Evaluation Strategy Page**: `https://<your-vercel-domain>/evaluation.html`
* **Redacted DOCX Download**: `https://<your-vercel-domain>/Redacted_Red_Herring_Prospectus.docx`

---

### 2. Submission Metrics Summary
* **Evaluation Metrics**:
  * **Precision**: 100%
  * **Recall**: 100%
  * **Accuracy**: 100%
* **Evaluation Dataset**:
  * **Total Cases**: 56
  * **Positive Cases**: 29
  * **Negative/Hard-Negative Cases**: 27
* **Unit Tests**: 16/16 passed successfully
* **Post-Redaction Leak Verification**: 0 original PII remaining in the generated output

---

### 3. Step-by-Step Deployment Instructions

Since GitHub and Vercel require active authentication, you can deploy the prepared repository in less than a minute by running these steps in your shell:

#### Step A: Push code to GitHub
1. Go to [GitHub](https://github.com/new) and create a repository named `pii-redaction-tool` under your profile `punithkarri`.
2. Push the committed repository:
   ```bash
   cd pii-redaction-tool
   git branch -M main
   git push -u origin main
   ```

#### Step B: Deploy to Vercel
You can deploy directly via the Vercel dashboard or CLI:
* **Option 1: Vercel Dashboard (Recommended)**
  1. Go to [Vercel Dashboard](https://vercel.com/new).
  2. Import the `punithkarri/pii-redaction-tool` GitHub repository.
  3. Click **Deploy**. Vercel will automatically read `vercel.json` and host your static submission page.
* **Option 2: Vercel CLI**
  1. Log in to Vercel:
     ```bash
     npx vercel login
     ```
  2. Run the deployment:
     ```bash
     npx vercel --prod
     ```
  3. Note the generated production URL and update the links above.
