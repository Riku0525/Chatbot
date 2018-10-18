(function() {
    'use strict';
    // ----------------------------------------------------
    // Chat Details
    // ----------------------------------------------------

    let chat = {
        messages: [],
        room:  undefined,
        userId: undefined,
        currentUser: undefined,
    }


    // ----------------------------------------------------
    // Targeted Elements
    // ----------------------------------------------------

    const chatPage   = $(document)
    const chatWindow = $('.chatbubble')
    const chatHeader = chatWindow.find('.unexpanded')
    const chatBody   = chatWindow.find('.chat-window')


    // ----------------------------------------------------
    // Helpers
    // ----------------------------------------------------

    let helpers = {
        /**
         * Toggles the display of the chat window.
         */
        ToggleChatWindow: function () {
            chatWindow.toggleClass('opened')
        },

        /**
         * Show the appropriate display screen. Login screen
         * or Chat screen.
         */
        ShowAppropriateChatDisplay: function () {
            helpers.ShowChatRoomDisplay()
        },

        /**
         * Show the enter details form
         */
        ShowChatInitiationDisplay: function () {
            chatBody.find('.chats').addClass('active')
        },

        /**
         * Show the chat room messages dislay.
         */
        ShowChatRoomDisplay: function () {
            chatBody.find('.chats').addClass('active')
            chatBody.find('.input, .messages').show()
        },

        /**
         * Append a message to the chat messages UI.
         */
        NewChatMessage: function (message) {
            if (chat.messages[message.id] === undefined) {
                const messageClass = message.sender.id !== chat.userId ? 'support' : 'user'

                chatBody.find('ul.messages').append(
                    `<li class="clearfix message ${messageClass}">
                        <div class="sender">${message.sender.name}</div>
                        <div class="message">${message.text}</div>
                    </li>`
                )

                chat.messages[message.id] = message

                chatBody.scrollTop(chatBody[0].scrollHeight)
            }
        },

        /**
         * Send a message to the chat channel
         */
        SendMessageToSupport: function (evt) {
            evt.preventDefault()

            const message = $('#newMessage').val().trim()

            chat.currentUser.sendMessage(
                {text: message, roomId: chat.room.id},
                msgId => { console.log("Message added!") },
                error => { console.log(`Error adding message to ${chat.room.id}: ${error}`) }
            )

            $('#newMessage').val('')
        },

        /**
         * Logs user into a chat session
         */
        LogIntoChatSession: function (evt) {
            // Disable the form
            helpers.ShowChatRoomDisplay()
            evt.preventDefault()
        }
    }


    // ----------------------------------------------------
    // Register page event listeners
    // ----------------------------------------------------

    chatPage.ready(helpers.LogIntoChatSession)
    chatHeader.on('click', helpers.ToggleChatWindow)
    chatBody.find('#messageSupport').on('submit', helpers.SendMessageToSupport)
}())