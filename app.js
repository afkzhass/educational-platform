// Создание логотипа
function createLogo() {
  const logoContainer = document.querySelector('.logo-text');
  if (logoContainer) {
    logoContainer.innerHTML = `
      <span class="logo-main">📚</span>
      <span class="logo-title">ЕдПлатформа</span>
    `;
  }
}

// Заполнение курсов
const courses = [
  { id: 1, title: { ru: 'Математика', kk: 'Математика', en: 'Mathematics' }, class: '5 класс', topics: 12 },
  { id: 2, title: { ru: 'Физика', kk: 'Физика', en: 'Physics' }, class: '7 класс', topics: 10 },
  { id: 3, title: { ru: 'Биология', kk: 'Биология', en: 'Biology' }, class: '6 класс', topics: 8 },
  { id: 4, title: { ru: 'История Казахстана', kk: 'Қазақстан тарихы', en: 'History of Kazakhstan' }, class: '8 класс', topics: 15 },
];

const classNames = ['5 класс', '6 класс', '7 класс', '8 класс'];
let language = 'ru';
let activeClass = '5 класс';

const courseGrid = document.getElementById('course-grid');
const classButtons = document.getElementById('class-buttons');
const activeClassInfo = document.getElementById('active-class-info');
const heroTitle = document.getElementById('hero-title');
const heroSubtitle = document.getElementById('hero-subtitle');

const langButtons = document.querySelectorAll('.language-switcher button');
langButtons.forEach(btn => {
  btn.addEventListener('click', () => {
    language = btn.getAttribute('data-lang');
    renderApp();
  });
});

const aiMessages = document.getElementById('ai-messages');
const aiInput = document.getElementById('ai-input');
const aiSend = document.getElementById('ai-send');
const aiClose = document.getElementById('ai-close');
const aiWidget = document.getElementById('ai-widget');

aiSend.addEventListener('click', () => {
  const msg = aiInput.value.trim();
  if (!msg) return;
  const bubble = document.createElement('div');
  bubble.textContent = `Вы: ${msg}`;
  bubble.style.marginBottom = '0.5rem';
  aiMessages.appendChild(bubble);
  aiInput.value = '';
  setTimeout(() => {
    const answer = document.createElement('div');
    answer.textContent = `AI: Я получил ваше сообщение: "${msg}"`;
    answer.style.fontWeight = '600';
    aiMessages.appendChild(answer);
    aiMessages.scrollTop = aiMessages.scrollHeight;
  }, 400);
});

aiClose.addEventListener('click', () => {
  aiWidget.style.display = 'none';
});

function renderCourses() {
  courseGrid.innerHTML = '';
  const filtered = courses.filter(c => c.class === activeClass);
  if (filtered.length === 0) {
    courseGrid.innerHTML = `<p>${language === 'ru' ? 'Курсы не найдены' : language === 'kk' ? 'Курстар табылмады' : 'No courses found'}</p>`;
    return;
  }
  filtered.forEach(course => {
    const card = document.createElement('div');
    card.className = 'course-card';
    card.innerHTML = `
      <h3>${course.title[language]}</h3>
      <p>${language === 'ru' ? 'Класс' : language === 'kk' ? 'Сынып' : 'Class'}: ${course.class}</p>
      <p>${language === 'ru' ? 'Темы' : language === 'kk' ? 'Тақырыптар' : 'Topics'}: ${course.topics}</p>
    `;
    courseGrid.appendChild(card);
  });
}

function renderClassButtons() {
  classButtons.innerHTML = '';
  classNames.forEach(cls => {
    const button = document.createElement('button');
    button.textContent = cls;
    button.style.marginRight = '10px';
    button.style.padding = '8px 12px';
    button.style.borderRadius = '8px';
    button.style.border = activeClass === cls ? '2px solid var(--dark-blue)' : '1px solid #ccc';
    button.style.cursor = 'pointer';
    button.addEventListener('click', () => {
      activeClass = cls;
      renderApp();
    });
    classButtons.appendChild(button);
  });
}

function renderApp() {
  heroTitle.textContent = language === 'ru' ? 'Образовательная платформа' : language === 'kk' ? 'Білім беру платформа' : 'Education Platform';
  heroSubtitle.textContent = language === 'ru' ? 'Выбирайте курсы, изучайте материалы и развивайтесь!' : language === 'kk' ? 'Курстарды таңдаңыз, материалдарды зерттеңіз және дамыңыз!' : 'Choose courses, learn materials, and grow!';

  activeClassInfo.textContent = `${language === 'ru' ? 'Текущий класс' : language === 'kk' ? 'Ағымдағы класс' : 'Active class'}: ${activeClass}`;
  renderCourses();
  renderClassButtons();
}

createLogo();
renderApp();
