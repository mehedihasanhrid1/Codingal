document.addEventListener("DOMContentLoaded", ()=>{
    const clockElement = document.getElementById("clock");
    
    function updateClock(){
        const now = new Date();
        let hours = now.getHours();
        const minutes = String(now.getMinutes()).padStart(2,"0");
        const seconds = String(now.getSeconds()).padStart(2,"0");

        const amPM = hours >= 12 ? "PM" : "AM";

        hours = hours % 12 || 12;

        clockElement.textContent = `${String(hours).padStart(2,"0")} : ${minutes} : ${seconds} ${amPM}`;
    }
    setInterval(updateClock, 1000);

    updateClock();
})