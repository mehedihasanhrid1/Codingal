function checkPalindrome(){
    const input = document.getElementById("textInput").value;

    const result = document.getElementById("result");

    const cleanedInput = input.replace(/[^a-zA-Z0-9]/g, '').toLowerCase();

    const reversed = cleanedInput.split('').reverse().join('');

    if (cleanedInput.length === 0) {
        result.innerHTML = "Please enter a valid string.";
    }
    else if (cleanedInput === reversed) {
        result.innerHTML = `"${input}" is a palindrome.`;
        result.style.color = "green";
    } 
    else {
        result.innerHTML = `"${input}" is not a palindrome.`;
        result.style.color = "red";
    }
}