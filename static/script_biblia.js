document.addEventListener('DOMContentLoaded', function() {
    const booksListAT = document.getElementById('booksListAT');
    const booksListNT = document.getElementById('booksListNT');
    const chaptersList = document.getElementById('chaptersList');
    const versesList = document.getElementById('versesList');
    const verseReference = document.getElementById('verseReference');
    const clearSelectionButton = document.getElementById('clearSelection');
    const backToTopButton = document.getElementById('backToTopButton');
    const noVerseReference = document.getElementById('noVerseReference');
    const bookInput = document.getElementById('search-books');
    const chapterInput = document.getElementById('search-chapters');
    const verseInput = document.getElementById('search-verses');
    const clearButton = document.getElementById('clear-selection');
    const suggestionsContainer = document.getElementById('suggestions-container');
    const suggestionsBContainer = document.getElementById('suggestions-bcontainer');
    const suggestionsVContainer = document.getElementById('suggestions-vcontainer');
    const output = document.getElementById('output');

    let bibleData = null;
    let element = null;
    let selectedBook = null;
    let selectedChapter = null;
    let selectedVerse = null;
    let ip = null;
    let token = null;
    let puerto = null;
    quickPresentation = false;

    document.getElementById("quick_presentation").addEventListener("change", function () {
        quickPresentation = this.checked; // True si está marcado, False si no
    });

    // Cargar los datos de la Biblia desde JSON
    fetch('/static/bible.json')
        .then(response => response.json())
        .then(data => {
            bibleData = data.books;

            // Filtrar y crear listas de libros del AT y NT con IDs únicos
            populateBooksList(bibleData.filter(b => b.number <= 39), booksListAT, 1);
            populateBooksList(bibleData.filter(b => b.number > 39), booksListNT, 40);
        })
        .catch(error => console.error('Error al cargar los datos de la Biblia:', error));
    
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

    // Función para llenar las listas de libros con IDs únicos
    function populateBooksList(books, listElement) {
        books.forEach((book, index) => {
            const li = document.createElement('li');
            li.textContent = capitalizeFirstLetter(book.name);
            li.setAttribute('data-type', 'libro');
            // Agregar una clase basada en el grupo del libro
            if (book.group) {
                li.classList.add(book.group); // Clase del grupo
            }
            li.addEventListener('click', () => {
                handleBookClick(li, book, index);
            });

            listElement.appendChild(li);
        });
    }

    function capitalizeFirstLetter(text) {
        return text.charAt(0).toUpperCase() + text.slice(1);
    }

    function handleBookClick(li, book, index) {
        selectedBook = book;
        seleccionar(li, 'book');
        loadChapters(book, index);
        updateReference(book.name, null, null);
        const chaptersPosition = chaptersList.getBoundingClientRect().top;
        const offset = 90; // Ajuste de desplazamiento
        window.scrollTo({
            top: chaptersPosition - offset,
            behavior: 'smooth'
        });
    }

    function seleccionar(li, type) {
        let selectedBook = document.querySelector('[data-type="libro"].selected');
        let selectedChapter = document.querySelector('[data-type="capitulo"].selected');
        let selectedVerse = document.querySelector('[data-type="versiculo"].selected');
        if (element && type === 'book') {
            selectedBook.classList.remove('selected');
        } else if (selectedChapter  && type === 'chapter') {
            selectedChapter.classList.remove('selected');
        } else if (selectedVerse && type === 'verse') {
            selectedVerse.classList.remove('selected');
        }
        li.classList.add('selected');
        element = li;
        
    }

    function loadChapters(book, bookIndex) {
        chaptersList.innerHTML = '';
        versesList.innerHTML = '';
        const totalChapters = book.content.reduce((max, item) => Math.max(max, parseInt(item.chapter)), 0);

        for (let i = 1; i <= totalChapters; i++) {
            const li = document.createElement('li')
            li.textContent = i;
            li.setAttribute('data-type', 'capitulo');
            li.addEventListener('click', () => {
                handleChapterClick(li, book, i);
            });
            chaptersList.appendChild(li);
        }
    }

    function handleChapterClick(li, book, value) {
        seleccionar(li, 'chapter');
        loadVerses(book, value);
        updateReference(book.name, value, null);
        // const versesPosition = document.querySelector('#versesList'); // Elemento a desplazar
        // versesPosition.scrollIntoView({
        //     behavior: 'smooth', 
        //     block: 'start', // Ajusta al inicio del elemento
        //     inline: 'nearest'
        // });

        const versesPosition = versesList.getBoundingClientRect().top;
        const offset = 90; // Ajuste de desplazamiento
        window.scrollTo({
            top: versesPosition + window.scrollY - offset,
            behavior: 'smooth'
        });
    }

    function loadVerses(book, chapter) {
        let ids = [];
        versesList.innerHTML = '';
        const verses = book.content.filter(item => parseInt(item.chapter) === chapter);
        
        verses.forEach(verse => {
            const li = document.createElement('li');
            li.textContent = `${verse.verse}. ${verse.content}`;
            li.setAttribute('data-type', 'versiculo');
            li.addEventListener('click', () => {
                ids = verses
                .filter(v => parseInt(v.verse) >= parseInt(verse.verse))
                .map(v => generateVerseID(book.number, chapter, v.verse));
                handleVerseClick(li, book, chapter, verses, verse.verse, ids);
            });
            versesList.appendChild(li);
        });
    }

    function handleVerseClick(li, book, chapter, verses, verse, ids = []) {
        seleccionar(li, 'verse');
        updateReference(book.name, chapter, verse);
        sendVerseSelection(book.number, chapter, verse, ids); // Llamar a la función para llamar al versículo seleccionado desde Holyrics;
    }

    function updateReference(bookName, chapter, verse) {
        let reference = capitalizeFirstLetter(bookName);
        if (chapter !== null) {
            reference += ` ${chapter}`;
        }
        if (verse !== null) {
            reference += `:${verse}`;
        }
        verseReference.textContent = reference;
        clearSelectionButton.style.display = reference ? 'block' : 'none';
        noVerseReference.style.display = reference ? 'none' : 'block';
    }

    function generateVerseID(bookNumber, chapter, verse) {
        const bookID = String(bookNumber).padStart(2, '0');
        const chapterID = String(chapter).padStart(3, '0');
        const verseID = String(verse).padStart(3, '0');
        return bookID + chapterID + verseID;
    }

    function sendVerseSelection(bookNumber, chapter, verse, ids) {
        const verseID = generateVerseID(bookNumber, chapter, verse);
        const url = `http://${ip}:${puerto}/api/ShowVerse?token=${token}`;
        const data = ids.length > 0
            ? { ids, quick_presentation: quickPresentation } // Usar el array de IDs si existe
            : { id: verseID, quick_presentation: quickPresentation };
        fetch(url, { 
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
         })
        .then(response => {
            if (response.ok) {
                console.log(`Versículo seleccionado: ${bookNumber} ${chapter}:${verse}`);
                output.textContent = '';
            } else {
                console.error('Error al seleccionar el versículo:', response.statusText);
                output.textContent = 'Error en la solicitud.';
            }
        })
        .catch(error => {
            console.error('Error en la solicitud:', error);
            output.textContent = '';
            output.textContent = `Error en la solicitud: ${error.message}`;
        });
    }

    // Función para filtrar libros
    bookInput.addEventListener('input', () => {
        const searchValue = bookInput.value.toLowerCase();
        
        // Filtrar libros basados en la búsqueda
        const bookMatches = bibleData.filter(book => book.name.toLowerCase().startsWith(searchValue));

        if (bookMatches.length === 1) {
            // Autocompletar si solo queda un libro
            selectedBook = bookMatches[0];
            bookInput.value = selectedBook.name;
            suggestionsBContainer.innerHTML = '';
            suggestionsBContainer.style.display = 'none';

            // Buscar el <li> correspondiente en la lista
            const bookListItems = document.querySelectorAll('[data-type="libro"]');
            const matchingLi = Array.from(bookListItems).find(li => 
                li.textContent.trim().toLowerCase() === selectedBook.name.toLowerCase()
            );
            if (matchingLi) {
                // Simular el clic en el <li>
                matchingLi.click();
                //seleccionar(matchingLi, 'book');
            }
            // Pasar al campo de capítulos automáticamente
            chapterInput.focus();
            

        } else if (bookMatches.length > 1) {
            // Mostrar lista desplegable con coincidencias posibles
            showBookSuggestions(bookMatches);
        } else {
            selectedBook = null;
        }
    });

    // Función para mostrar sugerencias de libros
    function showBookSuggestions(bookMatches) {
        
        suggestionsBContainer.innerHTML = ''; // Limpiar sugerencias anteriores

        if (bookMatches.length === 0) {
            suggestionsBContainer.style.display = 'none'; // Ocultar si no hay coincidencias
            return;
        }

        bookMatches.forEach(book => {
            const suggestionElement = document.createElement('div');
            suggestionElement.className = 'suggestion';
            suggestionElement.textContent = book.name;
            suggestionElement.addEventListener('click', () => {
                selectedBook = book;
                bookInput.value = selectedBook.name;
                suggestionsBContainer.innerHTML = ''; // Limpiar sugerencias después de seleccionar
                suggestionsBContainer.style.display = 'none';
                
                // Buscar el <li> correspondiente en la lista
                const bookListItems = document.querySelectorAll('[data-type="libro"]');
                const matchingLi = Array.from(bookListItems).find(li => 
                    li.textContent.trim().toLowerCase() === selectedBook.name.toLowerCase()
                );
    
                if (matchingLi) {
                    // Simular el clic en el <li>
                    matchingLi.click();
                    //seleccionar(matchingLi, 'book');
                }

                // Pasar al campo de versículos automáticamente
                chapterInput.focus();
            });
            suggestionsBContainer.appendChild(suggestionElement);
        });
        // Mostrar el contenedor de sugerencias
        suggestionsBContainer.style.display = 'block';
        // Actualizar la posición del contenedor para que se muestre hacia arriba
        const rect = bookInput.getBoundingClientRect();
        suggestionsBContainer.style.left = `${rect.left}px`;
        suggestionsBContainer.style.width = `${rect.width}px`;
        suggestionsBContainer.style.bottom = `${window.innerHeight - rect.top}px`;
    }

    function handleChapterEvent(event) {
        if (!selectedBook) {
            alert('Primero selecciona un libro válido');
            return;
        }
    
        const totalChapters = getTotalChapters(selectedBook);
        let chapterList = [];
        for (let i = 1; i <= totalChapters; i++) {
            chapterList.push(i.toString());
        }
    
        const chapterValue = chapterInput.value;
        
    
        if (event.type === 'input') {
            const chapterMatches = chapterList.filter(chapter => chapter.startsWith(chapterValue));
            if (chapterMatches.length === 1) {
                // Autocompletar si solo queda un capítulo
                selectedChapter = chapterMatches[0];
                chapterInput.value = selectedChapter;
                suggestionsContainer.innerHTML = '';
                suggestionsContainer.style.display = 'none';

                const matchingChapter = Array.from(document.querySelectorAll('[data-type="capitulo"]'))
                .find(li => li.textContent.trim() === selectedChapter);
                if (matchingChapter) {
                    // Simular el clic en el <li>
                    matchingChapter.click();
                    //seleccionar(chapterUnique, 'chapter');
                }                
    
                // Pasar al campo de versículos automáticamente
                verseInput.focus();
            } else if (chapterMatches.length > 1) {
                // Mostrar lista desplegable con coincidencias posibles (opcional)
                showChapterSuggestions(chapterMatches);
            } else {
                selectedChapter = null;
            }
        }  else if (event.type === 'click') {
            selectedChapter = event.target.textContent.trim();
            chapterInput.value = selectedChapter;
            
            const matchingChapter = Array.from(document.querySelectorAll('[data-type="capitulo"]'))
            .find(li => li.textContent.trim() === selectedChapter);
            if (matchingChapter) {
                // Simular el clic en el <li>
                matchingChapter.click();
                //seleccionar(chapterUnique, 'chapter');
            }     
            // Ocultar sugerencias
            suggestionsContainer.innerHTML = '';
            suggestionsContainer.style.display = 'none';
        }  else if (event.type === 'keydown' && event.key === 'Tab') {
            const chapterMatches = chapterList.filter(chapter => chapter.startsWith(chapterValue));
            // Si hay coincidencias, selecciona la primera opción automáticamente
            if (chapterMatches.length > 0) {
                selectedChapter = chapterMatches[0];
                chapterInput.value = selectedChapter;

                const matchingChapter = Array.from(document.querySelectorAll('[data-type="capitulo"]'))
                .find(li => li.textContent.trim() === selectedChapter);
                if (matchingChapter) {
                    // Simular el clic en el <li>
                    matchingChapter.click();
                    //seleccionar(chapterUnique, 'chapter');
                }     
            }
            // Limpiar sugerencias y ocultar el contenedor
            suggestionsContainer.innerHTML = '';
            suggestionsContainer.style.display = 'none';
        } else {
            selectedChapter = null;
        }
    }

    // Función para mostrar sugerencias
    function showChapterSuggestions(chapterMatches) {
        suggestionsContainer.innerHTML = ''; // Limpiar sugerencias anteriores

        chapterMatches.forEach(chapter => {
            const suggestionElement = document.createElement('div');
            suggestionElement.className = 'suggestion';
            suggestionElement.textContent = chapter;
            suggestionsContainer.appendChild(suggestionElement);
        });

        // Mostrar el contenedor de sugerencias
        suggestionsContainer.style.display = 'block';
        const rect = chapterInput.getBoundingClientRect();
        
        suggestionsContainer.style.left = `${rect.left}px`;
        suggestionsContainer.style.width = `${rect.width}px`;
        suggestionsContainer.style.bottom = `${window.innerHeight - rect.top}px`;
    }
    
    // Asignar eventos al campo de entrada y contenedor de sugerencias
    chapterInput.addEventListener('input', handleChapterEvent);
    chapterInput.addEventListener('keydown', handleChapterEvent);
    suggestionsContainer.addEventListener('click', handleChapterEvent);

    
    // Funciones auxiliares
    function getTotalChapters(book) {
        return book.content.reduce((max, item) => Math.max(max, parseInt(item.chapter)), 0);
    }

    function handleVerseEvent(event) {
        if (!selectedBook || !selectedChapter) {
            return alert('Primero selecciona un libro y capítulo');
        }
        
        const verseValue = verseInput.value;
        const verseMatches = selectedBook.content.filter(verse => parseInt(verse.chapter) === parseInt(selectedChapter) && verse.verse.startsWith(verseValue));
        let verseList = [];

        verseMatches.forEach(verse => {
            verseList.push(verse.verse);
        });
    
        if (event.type === 'input') {
            const verseMatches = verseList.filter(verse => verse.startsWith(verseValue));
            if (verseMatches.length === 1) {
                selectedVerse = verseMatches[0];
                verseInput.value = selectedVerse;
                suggestionsVContainer.innerHTML = '';
                suggestionsVContainer.style.display = 'none';

                const matchingVerse = Array.from(document.querySelectorAll('[data-type="versiculo"]'))
                .find(li => li.textContent.trim().startsWith(selectedVerse + '. '));
                if (matchingVerse) {
                    // Simular el clic en el <li>
                    matchingVerse.click();
                    //seleccionar(chapterUnique, 'chapter');
                }
            } else if (verseMatches.length > 1) {
                showVerseSuggestions(verseMatches);
            } else {
                selectedVerse = null;
            }
        } else if (event.type === 'click') { //&& event.target.classList.contains('suggestion')) {
            selectedVerse = event.target.textContent.trim();
            verseInput.value = selectedVerse;
            suggestionsVContainer.innerHTML = '';
            suggestionsVContainer.style.display = 'none';

            const matchingVerse = Array.from(document.querySelectorAll('[data-type="versiculo"]'))
                .find(li => li.textContent.trim().startsWith(selectedVerse + '. '));
                if (matchingVerse) {
                    // Simular el clic en el <li>
                    matchingVerse.click();
                    //seleccionar(chapterUnique, 'chapter');
                }
        } else if (event.type === 'keydown' && event.key === 'Enter') {
            const verseMatches = verseList.filter(verse => verse.startsWith(verseValue));
            if (verseMatches.length > 0) {
                selectedVerse = verseMatches[0];
                verseInput.value = selectedVerse;

                const matchingVerse = Array.from(document.querySelectorAll('[data-type="versiculo"]'))
                .find(li => li.textContent.trim().startsWith(selectedVerse + '. '));
                if (matchingVerse) {
                    // Simular el clic en el <li>
                    matchingVerse.click();
                    //seleccionar(chapterUnique, 'chapter');
                }
            }
            suggestionsVContainer.innerHTML = '';
            suggestionsVContainer.style.display = 'none';
        }

    }

    function showVerseSuggestions(verseMatches) {
        suggestionsVContainer.innerHTML = ''; // Limpiar sugerencias anteriores

        verseMatches.forEach(verse => {
            const suggestionElement = document.createElement('div');
            suggestionElement.className = 'suggestion';
            suggestionElement.textContent = verse;
            suggestionsVContainer.appendChild(suggestionElement);
        });

        // Mostrar el contenedor de sugerencias
        suggestionsVContainer.style.display = 'block';
        const rect = verseInput.getBoundingClientRect();
        suggestionsVContainer.style.left = `${rect.left}px`;
        suggestionsVContainer.style.width = `${rect.width}px`;
        suggestionsVContainer.style.bottom = `${window.innerHeight - rect.top}px`;
    }
    // Limpiar la selección
    clearButton.addEventListener('click', () => {
        bookInput.value = '';
        chapterInput.value = '';
        verseInput.value = '';
        selectedBook = null;
        selectedChapter = null;
        selectedVerse = null;
        bookInput.focus();
    });

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

    // Función para limpiar la selección
    function clearSelection() {
        //let selectedElement = document.querySelectorAll('.selected');

        let selectedBook = document.querySelector('[data-type="libro"].selected');
        let selectedChapter = document.querySelector('[data-type="capitulo"].selected');
        let selectedVerse = document.querySelector('[data-type="versiculo"].selected');
        if (selectedBook) {
            selectedBook.classList.remove('selected');
        } else if (selectedChapter) {
            selectedChapter.classList.remove('selected');
        } else if (selectedVerse) {
            selectedVerse.classList.remove('selected');
        }

        selectedBook = null;
        selectedChapter = null;
        selectedVerse = null;
        element = null;
        chaptersList.innerHTML = '';
        versesList.innerHTML = '';

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

    // function sendActionNext() {
    //     const url = `http://${ip}:${puerto}/api/ActionNext?token=${token}`;
    //     const data = {};

    //     fetch(url, { 
    //         method: 'POST',
    //         headers: {
    //             'Content-Type': 'application/json',
    //         },
    //         body: JSON.stringify(data),
    //      })
    //         .then(response => {
    //             if (response.ok) {
    //                 console.log('ActionNext enviado correctamente');
    //                 setTimeout(() => {
    //                     updateReferenceFromHolyrics();
    //                 }, 300);
    //             } else {
    //                 console.error('Error al enviar ActionNext:', response.statusText);
    //             }
    //         })
    //         .catch(error => {
    //             console.error('Error en la solicitud:', error);
    //         });
    // }

    // function sendActionPrevious() {
    //     const url = `http://${ip}:${puerto}/api/ActionPrevious?token=${token}`;
    //     const data = {};

    //     fetch(url, { 
    //         method: 'POST',
    //         headers: {
    //             'Content-Type': 'application/json',
    //         },
    //         body: JSON.stringify(data),
    //      })
    //         .then(response => {
    //             if (response.ok) {
    //                 console.log('ActionPrevious enviado correctamente');
    //                 setTimeout(() => {
    //                     updateReferenceFromHolyrics();
    //                 }, 300);
    //             } else {
    //                 console.error('Error al enviar ActionPrevious:', response.statusText);
    //             }
    //         })
    //         .catch(error => {
    //             console.error('Error en la solicitud:', error);
    //         });
    // }

    function sendCloseCurrentPresentation() {
        const url = quickPresentation 
        ? `http://${ip}:${puerto}/api/CloseCurrentQuickPresentation?token=${token}` 
        : `http://${ip}:${puerto}/api/CloseCurrentPresentation?token=${token}`;
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
                    output.textContent = '';
                    
                } else {
                    console.error('Error al enviar CloseCurrentPresentation:', response.statusText);
                    output.textContent = 'Error en la solicitud.';
                }
            })
            .catch(error => {
                console.error('Error en la solicitud:', error);
                output.textContent = '';
                output.textContent = `Error en la solicitud: ${error.message}`;
            });
    }
    
    // Función para obtener la referencia del versículo proyectado en Holyrics
    // function updateReferenceFromHolyrics() {
    //     const jsonURL = `http://${ip}/stage-view/text.json?html_type=1`;
    
    //     fetch(jsonURL)
    //         .then(response => {
    //             if (!response.ok) {
    //                 throw new Error('Network response was not ok');
    //             }
    //             return response.json();
    //         })
    //         .then(data => {
    //             // Acceder al campo `header`
    //             const headerText = data.map.header;

    //             // Extraer el contenido entre las etiquetas <desc> y </desc>
    //             const descMatch = headerText.match(/<desc>(.*?)<\/desc>/);
    //             if (descMatch && descMatch[1]) {
    //                 const verseReference = descMatch[1];
    //                 console.log("Referencia del versículo:", verseReference);

    //                 // Actualizar el DOM o realizar acciones necesarias
    //                 document.getElementById('verseReference').textContent = verseReference;
    //             } else {
    //                 console.error("No se encontró el contenido dentro de <desc>.");
    //             }
    //         })
    //         .catch(error => {
    //             console.error('Error al obtener el JSON:', error);
    //         });
    // }

    // Agregar evento para la navegación por teclado

    // document.addEventListener('keydown', function(event) {
    //     if (event.key === 'ArrowRight') {
    //         // Navegar al siguiente versículo
    //         sendActionNext();
    //     } else if (event.key === 'ArrowLeft') {
    //         // Navegar al versículo anterior
    //         sendActionPrevious();
    //     } else if (event.key === 'Escape') {
    //         // Borrar la selección
    //         clearSelection();
    //         sendCloseCurrentPresentation();
    //     }
    // });

    document.addEventListener('keydown', function(event) {
        if (event.key === 'Escape') {
            // Borrar la selección            
            clearSelection();            
            sendCloseCurrentPresentation();
        }
    });
    
    document.addEventListener('keydown', (event) => {
        if (event.key === 'ArrowRight' || event.key === 'ArrowLeft') {
            // Encuentra el versículo actualmente seleccionado
            const currentSelected = document.querySelector('[data-type="versiculo"].selected');
    
            if (currentSelected) {
                let targetVerse = null;
    
                if (event.key === 'ArrowRight') {
                    // Avanza al siguiente versículo
                    targetVerse = currentSelected.nextElementSibling;
                } else if (event.key === 'ArrowLeft') {
                    // Retrocede al versículo anterior
                    targetVerse = currentSelected.previousElementSibling;
                }
    
                if (targetVerse) {
                    // Simula un clic en el versículo correspondiente
                    targetVerse.click();
    
                    // Cambia la clase 'selected'
                    currentSelected.classList.remove('selected');
                    targetVerse.classList.add('selected');
                }
            } else {
                // Si no hay un versículo seleccionado, selecciona el primero para ArrowRight
                // O el último para ArrowLeft
                const verses = document.querySelectorAll('li');
                if (verses.length > 0) {
                    const initialVerse = event.key === 'ArrowRight' ? verses[0] : verses[verses.length - 1];
                    initialVerse.click();
                    initialVerse.classList.add('selected');
                }
            }
        }
    });
    

    // Asignar eventos al campo de entrada y contenedor de sugerencias
    verseInput.addEventListener('input', handleVerseEvent);
    verseInput.addEventListener('keydown', handleVerseEvent);
    suggestionsVContainer.addEventListener('click', handleVerseEvent);
});
