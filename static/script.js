document.addEventListener('DOMContentLoaded', function() {
    const booksListAT = document.getElementById('booksListAT');
    const booksListNT = document.getElementById('booksListNT');
    const chaptersList = document.getElementById('chaptersList');
    const versesList = document.getElementById('versesList');
    const verseReference = document.getElementById('verseReference');
    const clearSelectionButton = document.getElementById('clearSelection');
    const backToTopButton = document.getElementById('backToTopButton');
    const noVerseReference = document.getElementById('noVerseReference');
    let selectedElement = null;
    let bibleData = null; // Para almacenar los datos de la Biblia cargados
    
    // Variables para rastrear la selección actual
    let currentBookIndex = null;
    let currentChapter = null;
    let currentVerse = null;

    // Variables para almacenar la configuración del archivo config.json
    let ip = null;
    let token = null;
    let puerto = null;

    // Cargar el archivo config.json
    fetch('/api/config')
        .then(response => response.json())
        .then(config => {
            ip = config.ip;
            token = config.token;
            puerto = config.puerto;

        })
        .catch(error => {
            console.error('Error al cargar el archivo config.json:', error);
        });

    // Agregar evento para la navegación por teclado
    document.addEventListener('keydown', function(event) {
        if (event.key === 'ArrowRight') {
            // Navegar al siguiente versículo
            sendActionNext();
        } else if (event.key === 'ArrowLeft') {
            // Navegar al versículo anterior
            sendActionPrevious();
        } else if (event.key === 'Escape') {
            // Borrar la selección
            clearSelection();
            sendCloseCurrentPresentation();
        }
    });

    // Funciones auxiliares
    function getTotalChapters(book) {
        return book.content.reduce((max, item) => Math.max(max, parseInt(item.chapter)), 0);
    }

    

    // Mostrar el botón cuando el usuario se desplaza hacia abajo
    window.addEventListener('scroll', function() {
        if (window.scrollY > 50) {
            backToTopButton.style.display = 'block';
        } else {
            backToTopButton.style.display = 'none';
        }
    });

    // Volver al inicio cuando se hace clic en el botón
    backToTopButton.addEventListener('click', function() {
        window.scrollTo({ top: 0, behavior: 'smooth' });
    });

    // Ocultar el botón de borrar al inicio si no hay referencia
    clearSelectionButton.style.display = 'none';


    function selectElement(el, type, value) {
        if (selectedElement) {
            selectedElement.classList.remove('selected');
        }
        el.classList.add('selected');
        selectedElement = el;

        if (type === 'book') {
            currentBookIndex = value;
            currentChapter = null;
            currentVerse = null;
        } else if (type === 'chapter') {
            currentChapter = value;
            currentVerse = null;
        } else if (type === 'verse') {
            currentVerse = value;
        }
    }

    // Función para limpiar la selección
    function clearSelection() {
        if (selectedElement) {
            selectedElement.classList.remove('selected');
            selectedElement = null;
        }
        currentBookIndex = null;
        currentChapter = null;
        currentVerse = null;

        verseReference.textContent = ''; // Limpia la referencia
        noVerseReference.style.display = 'block'; // Muestra de nuevo el título
        clearSelectionButton.style.display = 'none'; // Oculta el botón de borrar
        sendCloseCurrentPresentation();

         // Desplazarse al inicio de la página
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    }

    clearSelectionButton.addEventListener('click', clearSelection);

    // Cargar la Biblia desde el archivo JSON
    fetch('/static/bible.json')
        .then(response => response.json())
        .then(data => {
            bibleData = data.books; // Guardar los datos de la Biblia

            // Filtrar libros del AT y NT
            const booksAT = bibleData.filter(book => parseInt(book.number) <= 39); // Libros del AT
            const booksNT = bibleData.filter(book => parseInt(book.number) > 39); // Libros del NT

            // Llenar la lista de libros del AT y NT
            populateBooksList(booksAT, booksListAT);
            populateBooksList(booksNT, booksListNT);

            // Aplicar truncamiento a los nombres de los libros
            truncateBookNames();

        })
        .catch(error => {
            console.error('Error al cargar el archivo JSON:', error);
        });


    function populateBooksList(books, listElement) {
        books.forEach((book, index) => {
            let li = document.createElement('li');
            li.textContent = capitalizeFirstLetter(book.name);
            li.addEventListener('click', function() {
                selectElement(li, 'book', index);
                loadChapters(book, index);
                updateReference(book.name, null, null);

                // Obtener la posición de la lista de capítulos
                const chaptersPosition = chaptersList.getBoundingClientRect().top;
                const offset = 90; // Ajuste de desplazamiento (puedes ajustar este valor)

                // Desplazarse con precisión
                window.scrollBy({
                    top: chaptersPosition - offset, // Desplaza un poco menos de lo necesario
                    behavior: 'smooth' });
            });
            listElement.appendChild(li);
        });
    }

    // Función para truncar los nombres de los libros
    function truncateBookNames() {
        const maxBookNameLength = 7; // Ajusta la longitud máxima según sea necesario
        const bookButtons = document.querySelectorAll('.books-column li');
        bookButtons.forEach(button => {
            let text = button.textContent.trim();
            if (text.length > maxBookNameLength) {
                button.textContent = text.substring(0, maxBookNameLength) + '...';
            }
        });
    }

    // Función para cargar los capítulos de un libro seleccionado
    function loadChapters(book, bookIndex) {
        chaptersList.innerHTML = '';
        versesList.innerHTML = '';

        // Obtener el total de capítulos de un libro
        const totalChapters = getTotalChapters(book);

        for (let i = 1; i <= totalChapters; i++) {
            let li = document.createElement('li');
            li.textContent = i;
            li.addEventListener('click', function() {
                selectElement(li, 'chapter', i);
                loadVerses(book, i, bookIndex); // Cargar versículos del capítulo seleccionado
                updateReference(book.name, i, null);

                // Obtener la posición de la lista de versículos
                const versesPosition = versesList.getBoundingClientRect().top;
                const offset = 90; // Ajuste de desplazamiento (ajusta este valor si es necesario)

                // Desplazarse con precisión
                window.scrollBy({
                    top: versesPosition - offset, // Ajustar desplazamiento
                    behavior: 'smooth'
                });
            });
            chaptersList.appendChild(li);
        }
    }

    // Función para cargar los versículos de un capítulo seleccionado
    function loadVerses(book, chapter) {
        versesList.innerHTML = '';

        // Filtrar los versículos del capítulo seleccionado
        const verses = book.content.filter(item => parseInt(item.chapter) === chapter);

        verses.forEach(verse => {
            let li = document.createElement('li');
            li.textContent = verse.verse;
            li.addEventListener('click', function() {
                selectElement(li, 'verse', parseInt(verse.verse));
                updateReference(book.name, chapter, verse.verse);
                
                // Llamar a la función para llamar al versículo seleccionado desde Holyrics
                sendVerseSelection(book.number, chapter, verse.verse);
            });
            versesList.appendChild(li);
        });
    }


    // Función para actualizar la referencia seleccionada
    function updateReference(book, chapter, verse) {
        let reference = capitalizeFirstLetter(book);
        if (chapter !== null) {
            reference += ` ${chapter}`;
        }
        if (verse !== null) {
            reference += `:${verse}`;
        }
        verseReference.textContent = reference;

        // Mostrar el botón de borrar si hay algo en la referencia
        if (reference) {
            clearSelectionButton.style.display = 'block';
            noVerseReference.style.display = 'none';
        } else {
            clearSelectionButton.style.display = 'none';
            noVerseReference.style.display = 'block';
        }

        
    }

    // Función para capitalizar la primera letra de un texto
    function capitalizeFirstLetter(text) {
        return text.charAt(0).toUpperCase() + text.slice(1);
    }

    function generateVerseID(bookNumber, chapter, verse) {
        // Aseguramos que el número del libro tenga dos dígitos
        const bookID = String(bookNumber).padStart(2, '0');
        
        // Aseguramos que el número del capítulo tenga tres dígitos
        const chapterID = String(chapter).padStart(3, '0');
        
        // Aseguramos que el número del versículo tenga tres dígitos
        const verseID = String(verse).padStart(3, '0');
        
        // Retornamos el ID concatenado
        return bookID + chapterID + verseID;
    }

    function sendVerseSelection(bookNumber, chapter, verse) {
        const verseID = generateVerseID(bookNumber, chapter, verse);
        const url = `http://${ip}:${puerto}/api/ShowVerse?token=${token}`;

        const data = { id: verseID };

        fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
        })
        .then(response => {
            if (response.ok) {
                console.log('Versículo enviado correctamente:', verseID);
                //updateReferenceFromHolyrics();
            } else {
                console.error('Error al enviar el versículo:', response.statusText);
            }
        })
        .catch(error => {
            console.error('Error en la solicitud:', error);
        });
    }

    function sendActionNext() {
        const url = `http://${ip}:${puerto}/api/ActionNext?token=${token}`;
        const data = {};

        fetch(url, { 
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
         })
            .then(response => {
                if (response.ok) {
                    console.log('ActionNext enviado correctamente');
                    setTimeout(() => {
                        updateReferenceFromHolyrics();
                    }, 300);
                } else {
                    console.error('Error al enviar ActionNext:', response.statusText);
                }
            })
            .catch(error => {
                console.error('Error en la solicitud:', error);
            });
    }

    function sendActionPrevious() {
        const url = `http://${ip}:${puerto}/api/ActionPrevious?token=${token}`;
        const data = {};

        fetch(url, { 
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
         })
            .then(response => {
                if (response.ok) {
                    console.log('ActionPrevious enviado correctamente');
                    setTimeout(() => {
                        updateReferenceFromHolyrics();
                    }, 300);
                } else {
                    console.error('Error al enviar ActionPrevious:', response.statusText);
                }
            })
            .catch(error => {
                console.error('Error en la solicitud:', error);
            });
    }

    function sendCloseCurrentPresentation() {
        const url = `http://${ip}:${puerto}/api/CloseCurrentPresentation?token=${token}`;
        const data = {};

        fetch(url, { 
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
         })
            .then(response => {
                if (response.ok) {
                    console.log('CloseCurrentPresentation enviado correctamente');
                    
                } else {
                    console.error('Error al enviar CloseCurrentPresentation:', response.statusText);
                }
            })
            .catch(error => {
                console.error('Error en la solicitud:', error);
            });
    }
    
    // Función para obtener la referencia del versículo proyectado en Holyrics
    function updateReferenceFromHolyrics() {
        const jsonURL = `http://${ip}/stage-view/text.json?html_type=1`;
    
        fetch(jsonURL)
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                // Acceder al campo `header`
                const headerText = data.map.header;

                // Extraer el contenido entre las etiquetas <desc> y </desc>
                const descMatch = headerText.match(/<desc>(.*?)<\/desc>/);
                if (descMatch && descMatch[1]) {
                    const verseReference = descMatch[1];
                    console.log("Referencia del versículo:", verseReference);

                    // Actualizar el DOM o realizar acciones necesarias
                    document.getElementById('verseReference').textContent = verseReference;
                } else {
                    console.error("No se encontró el contenido dentro de <desc>.");
                }
            })
            .catch(error => {
                console.error('Error al obtener el JSON:', error);
            });
    }
    
        
    
});
