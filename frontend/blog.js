const API_BASE = "http://localhost:8000";

// Utility
function getToken() {
  return localStorage.getItem("token");
}
function saveToken(token) {
  localStorage.setItem("token", token);
}
function requireAuth() {
  if (!getToken()) window.location.href = "login.html";
}

// Detect page
const path = window.location.pathname;

// ---------- Signup ----------
if (path.includes("signup.html")) {
  const form = document.getElementById("signupForm");
  if (form) {
    form.addEventListener("submit", async (e) => {
      e.preventDefault();
      const data = {
        username: form.username.value,
        email: form.email.value,
        password: form.password.value
      };
      const res = await fetch(`${API_BASE}/signup`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data)
      });
      if (res.ok) {
        alert("Signup successful!");
        window.location.href = "login.html";
      } else {
        const error = await res.json();
        alert(error.detail || "Signup failed");
      }
    });
  }
}

// ---------- Login ----------
if (path.includes("login.html")) {
  const form = document.getElementById("loginForm");
  if (form) {
    form.addEventListener("submit", async (e) => {
      e.preventDefault();
      const data = new URLSearchParams();
      data.append("username", form.username.value);
      data.append("password", form.password.value);
      const res = await fetch(`${API_BASE}/login`, {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body: data
      });
      if (res.ok) {
        const result = await res.json();
        saveToken(result.access_token);
        alert("Login successful!");
        window.location.href = "dashboard.html";
      } else {
        const error = await res.json();
        alert(error.detail || "Login failed");
      }
    });
  }
}

// ---------- Dashboard ----------
if (path.includes("dashboard.html")) {
  requireAuth();
  const token = getToken();
  const blogForm = document.getElementById("blogForm");
  const blogList = document.getElementById("blogList");
  const logoutBtn = document.getElementById("logoutBtn");

  if (logoutBtn) {
    logoutBtn.addEventListener("click", () => {
      localStorage.removeItem("token");
      window.location.href = "login.html";
    });
  }

  if (blogForm) {
    blogForm.addEventListener("submit", async (e) => {
      e.preventDefault();
      const blogId = blogForm.blogId.value;
      const data = {
        title: blogForm.title.value,
        content: blogForm.content.value,
        image_url: blogForm.image_url.value
      };
      const method = blogId ? "PUT" : "POST";
      const url = blogId ? `${API_BASE}/blogs/${blogId}` : `${API_BASE}/blogs/`;

      const res = await fetch(url, {
        method,
        headers: {
          "Authorization": `Bearer ${token}`,
          "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
      });

      if (res.ok) {
        alert(blogId ? "Blog updated!" : "Blog posted!");
        blogForm.reset();
        loadBlogs();
      } else {
        const error = await res.json();
        alert(error.detail || "Failed to save blog");
      }
    });
  }

  async function loadBlogs() {
    blogList.innerHTML = "";
    const res = await fetch(`${API_BASE}/blogs/`, {
      headers: { "Authorization": `Bearer ${token}` }
    });
    if (res.ok) {
      const blogs = await res.json();
      blogs.forEach(blog => {
        const blogItem = document.createElement("div");
        blogItem.className = "blog-item";
        blogItem.innerHTML = `
          <h4>${blog.title}</h4>
          ${blog.image_url ? `<img src="${blog.image_url}" alt="Blog Image" style="max-width:300px;"><br>` : ""}
          <p>${blog.content}</p>
          <button onclick="editBlog(${blog.id}, '${blog.title}', '${blog.content}', '${blog.image_url || ''}')">Edit</button>
          <button onclick="deleteBlog(${blog.id})">Delete</button>
          <div>
            <input type="text" id="comment-${blog.id}" placeholder="Add a comment">
            <button onclick="addComment(${blog.id})">Comment</button>
          </div>
          <div id="comments-${blog.id}">
            ${blog.comments.map(c => `
              <p><strong>Comment:</strong> ${c.content}
              <button onclick="deleteComment(${c.id})">Delete</button></p>
            `).join("")}
          </div>
          <hr>
        `;
        blogList.appendChild(blogItem);
      });
    } else {
      const error = await res.json();
      alert(error.detail || "Failed to load blogs");
    }
  }

  window.editBlog = function (id, title, content, image_url) {
    blogForm.blogId.value = id;
    blogForm.title.value = title;
    blogForm.content.value = content;
    blogForm.image_url.value = image_url;
  };

  window.deleteBlog = async function (blogId) {
    const res = await fetch(`${API_BASE}/blogs/${blogId}`, {
      method: "DELETE",
      headers: { "Authorization": `Bearer ${token}` }
    });
    if (res.ok) {
      alert("Blog deleted!");
      loadBlogs();
    } else {
      const error = await res.json();
      alert(error.detail || "Failed to delete blog");
    }
  };

  window.addComment = async function (blogId) {
    const input = document.getElementById(`comment-${blogId}`);
    const content = input.value;
    if (!content) return alert("Comment cannot be empty");

    const res = await fetch(`${API_BASE}/comments/`, {
      method: "POST",
      headers: {
        "Authorization": `Bearer ${token}`,
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ blog_id: blogId, content })
    });

    if (res.ok) {
      input.value = "";
      loadBlogs();
    } else {
      const error = await res.json();
      alert(error.detail || "Failed to add comment");
    }
  };

  window.deleteComment = async function (commentId) {
    const res = await fetch(`${API_BASE}/comments/${commentId}`, {
      method: "DELETE",
      headers: { "Authorization": `Bearer ${token}` }
    });
    if (res.ok) {
      alert("Comment deleted!");
      loadBlogs();
    } else {
      const error = await res.json();
      alert(error.detail || "Failed to delete comment");
    }
  };

  loadBlogs();
}