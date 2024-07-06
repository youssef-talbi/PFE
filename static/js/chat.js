document.addEventListener("DOMContentLoaded", () => {
  const socket = io.connect();

  window.getAndDisplayChannels = function (departmentId) {
    if (!departmentId) {
      console.error("Department ID is not defined");
      showError("Department ID is not defined");
      return;
    }

    fetch(`/chat/get_channels/${encodeURIComponent(departmentId)}`)
      .then((response) => {
        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }
        return response.json();
      })
      .then((data) => {
        const channelList = document.getElementById("channelList");
        channelList.innerHTML = "";
        data.forEach((channel) => {
          const channelItem = document.createElement("a");
          channelItem.href = "#";
          channelItem.classList.add("channel-item");
          channelItem.setAttribute("data-id", channel.id);
          channelItem.textContent = channel.name;
          channelList.appendChild(channelItem);
        });
      })
      .catch((error) => {
        console.error("Error fetching channels:", error);
        showError("Failed to load channels: " + error.message);
      });
  };

  // Joining a channel
  const channelList = document.querySelector(".channel-list");
  channelList.addEventListener("click", (e) => {
    const channelId = e.target.getAttribute("data-id");
    if (channelId) {
      joinChannel(channelId);
    }
  });

  const sendMessage = () => {
    const message = document.getElementById("chatMessageInput").value.trim();
    if (message === "") return;
    const channelId = document.getElementById("channelIdInput").value;
    socket.emit("chatmsg", { msg: message, channel_id: channelId });
    document.getElementById("chatMessageInput").value = "";
  };

  function displayMessage(data) {
    const chats = document.getElementById("chats");
    const messageElement = document.createElement("div");
    messageElement.className = "message";
    messageElement.innerHTML = `<strong>${data.sender}</strong>: ${data.message} <span class="timestamp">${data.timestamp}</span>`;
    chats.appendChild(messageElement);
    chats.scrollTop = chats.scrollHeight; // Scroll to the bottom
  }

  document.querySelectorAll(".channel-item").forEach((item) => {
    item.addEventListener("click", () => {
      const channelId = item.dataset.id;
      getAndDisplayMessages(channelId);
      socket.emit("joinChannel", { channel_id: channelId });
    });
  });

  document
    .getElementById("sendMessageForm")
    .addEventListener("submit", function (event) {
      event.preventDefault();
      sendMessage();
    });
  // Event listener for receiving messages
  socket.on("receive_message", (data) => {
    const chats = document.getElementById("chats");
    const messageItem = document.createElement("div");
    messageItem.classList.add("message");
    messageItem.innerHTML = `<strong>${data.username}</strong>: ${data.message} <span>${data.timestamp}</span>`;
    chats.appendChild(messageItem);
  });

  // Receiving a message
  socket.on("message_received", (data) => {
    displayMessage(data);
  });
  function showError(message) {
    const errorMessage = document.getElementById("error-message");
    errorMessage.style.display = "block";
    errorMessage.textContent = message;
  }
  // function getAndDisplayChannels(departmentId) {
  //   fetch(`/chat/get_channels/${departmentId}`)
  //     .then((response) => {
  //       if (!response.ok) {
  //         throw new Error(`HTTP error! Status: ${response.status}`);
  //       }
  //       return response.json();
  //     })
  //     .then((data) => {
  //       const channelList = document.getElementById("channelList");
  //       channelList.innerHTML = "";
  //       data.forEach((channel) => {
  //         const channelItem = document.createElement("a");
  //         channelItem.href = "#";
  //         channelItem.classList.add("channel-item");
  //         channelItem.setAttribute("data-id", channel.id);
  //         channelItem.textContent = channel.name;
  //         channelList.appendChild(channelItem);
  //       });
  //     })
  //     .catch((error) => {
  //       console.error("Error fetching channels:", error);
  //     });
  // }

  function joinChannel(channelId) {
    socket.emit("joinChannel", { channel_id: channelId });
    document.getElementById("channelIdInput").value = channelId;

    // Clear the chat area
    document.getElementById("chats").innerHTML = "";

    // Fetch and display messages for the channel
    fetch(`/chat/get_messages/${channelId}`)
      .then((response) => response.json())
      .then((data) => {
        if (data.success) {
          const chats = document.getElementById("chats");
          data.messages.forEach((message) => {
            const messageElement = document.createElement("div");
            messageElement.classList.add("chat-message");
            messageElement.innerHTML = `
              <strong>${message.username}</strong>: ${message.message} <span class="timestamp">${message.timestamp}</span>
            `;
            chats.appendChild(messageElement);
          });
        }
      });
  }

  async function getAndDisplayMessages(channelId) {
    try {
      const response = await fetch(`/chat/get_messages/${channelId}`);
      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }
      const data = await response.json();

      const chatsDiv = document.getElementById("chats");
      chatsDiv.innerHTML = ""; // Clear previous messages

      for (const message of data.messages) {
        const messageElement = document.createElement("div");
        messageElement.classList.add("message");
        messageElement.innerHTML = `
                <span class="username">${message.username}:</span>
                <span class="message-text">${message.message}</span>
                <span class="timestamp">${message.timestamp}</span>
            `;
        chatsDiv.appendChild(messageElement);
      }

      chatsDiv.scrollTop = chatsDiv.scrollHeight;
      document.getElementById("channelIdInput").value = channelId;
    } catch (error) {
      console.error("Error fetching messages:", error);
    }
  }

  // Handle channel creation
  const createChannelForm = document.getElementById("createChannelForm");
  createChannelForm.addEventListener("submit", (e) => {
    e.preventDefault();
    const channelNameInput = document.getElementById("channelNameInput");
    const departmentSelect = document.getElementById("departmentSelect");
    const channelName = channelNameInput.value;
    const departmentId = departmentSelect.value;

    fetch("/chat/create_channel", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        channelName: channelName,
        departmentId: departmentId,
      }),
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.success) {
          // Add the new channel to the list
          const channelList = document.getElementById("channelList");
          const channelItem = document.createElement("a");
          channelItem.href = "#";
          channelItem.classList.add("channel-item");
          channelItem.setAttribute("data-id", data.channel_id);
          channelItem.textContent = channelName;
          channelList.appendChild(channelItem);
          // Close the modal
          $("#createChannelModal").modal("hide");
        }
      });
  });

  const workspaceItems = document.querySelectorAll(".workspace-item");
  workspaceItems.forEach((item) => {
    item.addEventListener("click", () => {
      const departmentId = item.dataset.id;
      getAndDisplayChannels(departmentId);
    });
  });

  if (workspaceItems.length > 0) {
    const initialDepartmentId = workspaceItems[0].dataset.id;
    getAndDisplayChannels(initialDepartmentId);
  }

  // Function to load messages for a channel
  function loadMessages(channelId) {
    fetch(`/chat/get_messages/${channelId}`)
      .then((response) => response.json())
      .then((data) => {
        if (!data.success) {
          showError("Failed to load messages");
          return;
        }
        const chats = document.getElementById("chats");
        chats.innerHTML = "";
        data.messages.forEach((msg) => {
          const messageItem = document.createElement("div");
          messageItem.classList.add("message");
          messageItem.innerHTML = `<strong>${msg.username}</strong>: ${msg.message} <span>${msg.timestamp}</span>`;
          chats.appendChild(messageItem);
        });
        document.getElementById("channelIdInput").value = channelId;
      })
      .catch((error) => {
        console.error("Failed to load messages: ", error);
        showError("Failed to load messages: " + error.message);
      });
  }
  // Ensure proper modal toggling
  $("#createChannelModal").on("shown.bs.modal", function () {
    $("#channelNameInput").trigger("focus");
  });

  // Send message event
  const sendMessageForm = document.getElementById("sendMessageForm");
  sendMessageForm.addEventListener("submit", (e) => {
    e.preventDefault();
    const messageInput = document.getElementById("chatMessageInput");
    const message = messageInput.value;
    const channelId = document.getElementById("channelIdInput").value;

    if (message.trim() !== "") {
      socket.emit("chatmsg", {
        channel_id: channelId,
        msg: message,
      });
      messageInput.value = "";
    }
  });
  // Event listener for sending messages
  document
    .getElementById("sendMessageForm")
    .addEventListener("submit", (event) => {
      event.preventDefault();
      const messageInput = document.getElementById("chatMessageInput");
      const channelId = document.getElementById("channelIdInput").value;
      const employeeId = document.getElementById("employeeIdInput").value;
      socket.emit("send_message", {
        message: messageInput.value,
        channel_id: channelId,
        employee_id: employeeId,
      });
      messageInput.value = "";
    });
  function showError(message) {
    const errorMessage = document.getElementById("error-message");
    errorMessage.textContent = message;
    errorMessage.style.display = "block";
    setTimeout(() => {
      errorMessage.style.display = "none";
    }, 5000);
  }
});
