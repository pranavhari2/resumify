async function generateCoverLetter() {
    const companyName = document.getElementById('companyName').value;
    const resume = document.getElementById('resume').value;
    // const resumeFile = document.getElementById('resume').files[0];
    const resultDiv = document.getElementById('result');

    // const formData = new FormData();
    // formData.append('company_name', companyName);
    // formData.append('resume', resumeFile);

    const response = await fetch('/generate-cover-letter', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({company: companyName, resume: resume}) 
    });

    const data = await response.json();
    resultDiv.textContent = data.cover_letter;
}