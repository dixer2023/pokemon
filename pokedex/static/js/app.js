(function () {
    const translations = {
        en: {
            brand: 'Pokedex',
            language: 'Language',
            theme_dark: 'Dark theme',
            theme_light: 'Light theme',
            back_to_pokedex: 'Back to Pokedex',
            evolution_line: 'Evolution Line',
            classification: 'Classification:',
            height: 'Height:',
            weight: 'Weight:',
            capture_rate: 'Capture Rate:',
            stats: 'Stats',
            total: 'Total',
            search_name: 'Search by name...',
            all_types: 'All types',
            no_results: 'No Pok\u00e9mon found',
            types: {
                grass: 'Grass',
                poison: 'Poison',
                fire: 'Fire',
                flying: 'Flying',
                water: 'Water',
                bug: 'Bug',
                normal: 'Normal',
                electric: 'Electric',
                ground: 'Ground',
                fairy: 'Fairy',
                fighting: 'Fighting',
                psychic: 'Psychic',
                rock: 'Rock',
                ghost: 'Ghost',
                ice: 'Ice',
                dragon: 'Dragon',
                dark: 'Dark',
                steel: 'Steel'
            }
        },
        uk: {
            brand: 'Покедекс',
            language: 'Мова',
            theme_dark: 'Темна тема',
            theme_light: 'Світла тема',
            back_to_pokedex: 'Назад до Покедексу',
            evolution_line: 'Лінія еволюції',
            classification: 'Класифікація:',
            height: 'Зріст:',
            weight: 'Вага:',
            capture_rate: 'Шанс впіймання:',
            stats: 'Характеристики',
            total: 'Разом',
            search_name: 'Пошук за назвою...',
            all_types: 'Всі типи',
            no_results: 'Покемонів не знайдено',
            types: {
                grass: 'Трава',
                poison: 'Отрута',
                fire: 'Вогонь',
                flying: 'Літаючий',
                water: 'Вода',
                bug: 'Комаха',
                normal: 'Нормальний',
                electric: 'Електричний',
                ground: 'Земля',
                fairy: 'Фея',
                fighting: 'Бойовий',
                psychic: 'Психічний',
                rock: 'Камінь',
                ghost: 'Привид',
                ice: 'Лід',
                dragon: 'Дракон',
                dark: 'Темний',
                steel: 'Сталь'
            }
        }
    };

    const languageSelect = document.getElementById('language-select');
    const themeToggle = document.getElementById('theme-toggle');

    function getLanguage() {
        const saved = localStorage.getItem('ui-language');
        if (saved === 'en' || saved === 'uk') {
            return saved;
        }
        return 'en';
    }

    function getTheme() {
        const savedTheme = localStorage.getItem('ui-theme');
        if (savedTheme === 'dark' || savedTheme === 'light') {
            return savedTheme;
        }
        return 'light';
    }

    function applyTheme(theme) {
        document.documentElement.setAttribute('data-theme', theme);
        localStorage.setItem('ui-theme', theme);
        const lang = getLanguage();
        if (themeToggle) {
            const key = theme === 'dark' ? 'theme_light' : 'theme_dark';
            themeToggle.textContent = translations[lang][key];
        }
    }

    function applyTypeTranslations(lang) {
        const typeMap = translations[lang].types;
        const typeElements = document.querySelectorAll('[data-type-name]');

        typeElements.forEach((el) => {
            const typeName = (el.getAttribute('data-type-name') || '').toLowerCase();
            el.textContent = typeMap[typeName] || typeName;
        });
    }

    function applyTypeFilterTranslations(lang) {
        const dict = translations[lang] || translations.en;
        const typeMap = dict.types || {};
        const options = document.querySelectorAll('#search-type option');

        options.forEach((option) => {
            const value = (option.value || '').toLowerCase();
            if (!value) {
                option.textContent = dict.all_types || 'All types';
                return;
            }
            option.textContent = typeMap[value] || option.textContent;
        });
    }

    function applyLanguage(lang) {
        const dict = translations[lang] || translations.en;
        document.documentElement.lang = lang;
        localStorage.setItem('ui-language', lang);

        const textNodes = document.querySelectorAll('[data-i18n]');
        textNodes.forEach((node) => {
            const key = node.getAttribute('data-i18n');
            if (dict[key]) {
                node.textContent = dict[key];
            }
        });

        applyTypeTranslations(lang);

        // placeholder translations
        document.querySelectorAll('[data-i18n-placeholder]').forEach((el) => {
            const key = el.getAttribute('data-i18n-placeholder');
            if (dict[key]) el.placeholder = dict[key];
        });

        applyTypeFilterTranslations(lang);

        if (languageSelect) {
            languageSelect.value = lang;
            languageSelect.setAttribute('aria-label', dict.language);
        }

        const theme = getTheme();
        if (themeToggle) {
            const key = theme === 'dark' ? 'theme_light' : 'theme_dark';
            themeToggle.textContent = dict[key];
        }
    }

    const initialTheme = getTheme();
    const initialLang = getLanguage();

    applyTheme(initialTheme);
    applyLanguage(initialLang);

    if (languageSelect) {
        languageSelect.addEventListener('change', (event) => {
            applyLanguage(event.target.value);
        });
    }

    if (themeToggle) {
        themeToggle.addEventListener('click', () => {
            const current = getTheme();
            const next = current === 'dark' ? 'light' : 'dark';
            applyTheme(next);
            applyLanguage(getLanguage());
        });
    }

    // --- Search / filter ---
    const searchName = document.getElementById('search-name');
    const searchType = document.getElementById('search-type');
    const noResults = document.getElementById('no-results');
    const searchCount = document.getElementById('search-count');
    const allCards = document.querySelectorAll('.pokemon-card');

    function filterCards() {
        const query = (searchName ? searchName.value.trim().toLowerCase() : '');
        const type = (searchType ? searchType.value.toLowerCase() : '');
        let visible = 0;
        allCards.forEach((card) => {
            const name = card.dataset.name || '';
            const t1 = card.dataset.type1 || '';
            const t2 = card.dataset.type2 || '';
            const matchName = !query || name.includes(query);
            const matchType = !type || t1 === type || t2 === type;
            const show = matchName && matchType;
            card.style.display = show ? '' : 'none';
            if (show) visible++;
        });
        if (noResults) noResults.style.display = visible === 0 ? 'block' : 'none';
        if (searchCount) searchCount.textContent = visible + ' / ' + allCards.length;
    }

    if (searchName) searchName.addEventListener('input', filterCards);
    if (searchType) searchType.addEventListener('change', filterCards);
    // init count
    if (searchCount && allCards.length) searchCount.textContent = allCards.length + ' / ' + allCards.length;
})();
