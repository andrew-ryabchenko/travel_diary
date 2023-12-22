const form = document.querySelector('form#new_entry');
const editorDataField = document.querySelector('input#editor_data');

form.onsubmit = (e) => {
    e.preventDefault();
    editor.save().then((outputData) => {
        editorDataField.value = JSON.stringify(outputData);
        form.submit();
      }).catch((error) => {
        console.error('Failed saving editor data: ', error);
      });
}

