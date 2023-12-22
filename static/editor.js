const editor = new EditorJS({
    holder: 'editorjs',
    tools: {
        image: {
            class: SimpleImage
        },
        header: {
            class: Header,
            config: {
              placeholder: 'Enter a header',
              levels: [1, 2, 3, 4],
              defaultLevel: 2
            }
        },
        list: {
            class: List,
            inlineToolbar: true,
            config: {
              defaultStyle: 'unordered'
            }
        },
        // image: {
        //     class: ImageTool,
        //     config: {
        //       endpoints: {
        //         byFile: 'http://localhost:8008/uploadFile', // Your backend file uploader endpoint
        //         byUrl: 'http://localhost:8008/fetchUrl', // Your endpoint that provides uploading by Url
        //       }
        //     }
        //   }
    },
    // autofocus: true,
    placeholder: 'Let`s write an awesome story!'
});

