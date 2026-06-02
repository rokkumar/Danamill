
// FAQ OPEN CLOSE

const faqQuestions = document.querySelectorAll(".faq-question");

faqQuestions.forEach((question) => {

    question.addEventListener("click", () => {

        const faqBox = question.parentElement;

        faqBox.classList.toggle("active");

    });

});