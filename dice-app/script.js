document.addEventListener("DOMContentLoaded", () => {
    const diceImage = document.getElementById("diceImage");
    const rollBtn = document.getElementById("rollBtn");

    const diceImages = [
        "dice-1.png",
        "dice-2.png",
        "dice-3.png",
        "dice-4.png",
        "dice-5.png",
        "dice-6.png"
    ];

    function rollDice() {
        const randomIndex = Math.floor(Math.random() * diceImages.length);
        diceImage.style.animation = "roll 1s ease-in-out"; 
        setTimeout(() => {
            diceImage.src = diceImages[randomIndex];
            diceImage.style.animation = ""; 
        }, 1000); 
    }

    rollBtn.addEventListener("click", rollDice);
});
