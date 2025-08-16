window.addEventListener('DOMContentLoaded', () => {
  const board = document.getElementById('board');
  const addBtn = document.getElementById('add-note');
  let noteCounter = 0;

  addBtn.addEventListener('click', () => {
    createNote({ id: noteCounter++, text: '', x: 100, y: 100 });
    saveNotes();
  });

  function createNote(data) {
    const note = document.createElement('div');
    note.className = 'note';
    note.style.left = (data.x || 100) + 'px';
    note.style.top = (data.y || 100) + 'px';
    note.dataset.id = data.id;

    const content = document.createElement('div');
    content.className = 'content';
    content.textContent = data.text || '';
    note.appendChild(content);
    board.appendChild(note);

    enableDrag(note);
    enableEdit(note, content);
  }

  function enableDrag(note) {
    let offsetX = 0, offsetY = 0, dragging = false;
    note.addEventListener('mousedown', (e) => {
      if (e.target.isContentEditable) return;
      dragging = true;
      offsetX = e.clientX - note.offsetLeft;
      offsetY = e.clientY - note.offsetTop;
      document.addEventListener('mousemove', onMouseMove);
      document.addEventListener('mouseup', onMouseUp);
      e.preventDefault();
    });

    function onMouseMove(e) {
      if (!dragging) return;
      note.style.left = (e.clientX - offsetX) + 'px';
      note.style.top = (e.clientY - offsetY) + 'px';
    }
    function onMouseUp() {
      if (dragging) {
        dragging = false;
        document.removeEventListener('mousemove', onMouseMove);
        document.removeEventListener('mouseup', onMouseUp);
        saveNotes();
      }
    }
  }

  function enableEdit(note, content) {
    note.addEventListener('dblclick', () => {
      content.contentEditable = 'true';
      content.focus();
      function handleClick(e) {
        if (!note.contains(e.target)) {
          content.contentEditable = 'false';
          document.removeEventListener('mousedown', handleClick);
          saveNotes();
        }
      }
      document.addEventListener('mousedown', handleClick);
    });
  }

  function saveNotes() {
    const data = Array.from(document.querySelectorAll('.note')).map(n => ({
      id: n.dataset.id,
      text: n.querySelector('.content').innerText,
      x: parseInt(n.style.left, 10),
      y: parseInt(n.style.top, 10)
    }));
    localStorage.setItem('notes', JSON.stringify(data));
  }

  function loadNotes() {
    const saved = JSON.parse(localStorage.getItem('notes') || '[]');
    saved.forEach(item => {
      createNote(item);
      noteCounter = Math.max(noteCounter, Number(item.id) + 1);
    });
    if (saved.length === 0) addBtn.click();
  }

  loadNotes();
});
