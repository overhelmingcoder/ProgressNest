// TrackMyJourney - Main JavaScript

// Import Bootstrap
const bootstrap = window.bootstrap

document.addEventListener("DOMContentLoaded", () => {
  // Initialize tooltips
  var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
  var tooltipList = tooltipTriggerList.map((tooltipTriggerEl) => new bootstrap.Tooltip(tooltipTriggerEl))

  // Initialize popovers
  var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'))
  var popoverList = popoverTriggerList.map((popoverTriggerEl) => new bootstrap.Popover(popoverTriggerEl))

  // Auto-hide alerts after 5 seconds
  setTimeout(() => {
    var alerts = document.querySelectorAll(".alert")
    alerts.forEach((alert) => {
      var bsAlert = new bootstrap.Alert(alert)
      bsAlert.close()
    })
  }, 5000)

  // Smooth scrolling for anchor links
  document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
    anchor.addEventListener("click", function (e) {
      e.preventDefault()
      const target = document.querySelector(this.getAttribute("href"))
      if (target) {
        target.scrollIntoView({
          behavior: "smooth",
          block: "start",
        })
      }
    })
  })

  // Progress bar animations
  function animateProgressBars() {
    const progressBars = document.querySelectorAll(".progress-bar")
    progressBars.forEach((bar) => {
      const width = bar.style.width || bar.getAttribute("aria-valuenow") + "%"
      bar.style.width = "0%"
      setTimeout(() => {
        bar.style.width = width
      }, 100)
    })
  }

  // Animate progress bars when they come into view
  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        animateProgressBars()
      }
    })
  })

  document.querySelectorAll(".progress").forEach((progress) => {
    observer.observe(progress)
  })

  // Form validation enhancements
  const forms = document.querySelectorAll(".needs-validation")
  forms.forEach((form) => {
    form.addEventListener("submit", (event) => {
      if (!form.checkValidity()) {
        event.preventDefault()
        event.stopPropagation()
      }
      form.classList.add("was-validated")
    })
  })

  // Dynamic search functionality
  const searchInputs = document.querySelectorAll("[data-search]")
  searchInputs.forEach((input) => {
    input.addEventListener("input", function () {
      const searchTerm = this.value.toLowerCase()
      const targetSelector = this.getAttribute("data-search")
      const targets = document.querySelectorAll(targetSelector)

      targets.forEach((target) => {
        const text = target.textContent.toLowerCase()
        if (text.includes(searchTerm)) {
          target.style.display = ""
        } else {
          target.style.display = "none"
        }
      })
    })
  })

  // Like button functionality
  document.addEventListener("click", (e) => {
    if (e.target.classList.contains("like-btn") || e.target.closest(".like-btn")) {
      e.preventDefault()
      const btn = e.target.classList.contains("like-btn") ? e.target : e.target.closest(".like-btn")
      const url = btn.getAttribute("data-url")

      fetch(url, {
        method: "POST",
        headers: {
          "X-CSRFToken": getCookie("csrftoken"),
          "Content-Type": "application/json",
        },
      })
        .then((response) => response.json())
        .then((data) => {
          if (data.success) {
            const icon = btn.querySelector("i")
            const count = btn.querySelector(".like-count")

            if (data.liked) {
              icon.classList.remove("far")
              icon.classList.add("fas", "text-danger")
              btn.classList.add("liked")
            } else {
              icon.classList.remove("fas", "text-danger")
              icon.classList.add("far")
              btn.classList.remove("liked")
            }

            if (count) {
              count.textContent = data.count
            }
          }
        })
        .catch((error) => {
          console.error("Error:", error)
        })
    }
  })

  // Image preview functionality
  const imageInputs = document.querySelectorAll('input[type="file"][accept*="image"]')
  imageInputs.forEach((input) => {
    input.addEventListener("change", (e) => {
      const file = e.target.files[0]
      if (file) {
        const reader = new FileReader()
        reader.onload = (e) => {
          let preview = document.querySelector(`#${input.id}-preview`)
          if (!preview) {
            preview = document.createElement("img")
            preview.id = `${input.id}-preview`
            preview.className = "img-thumbnail mt-2"
            preview.style.maxWidth = "200px"
            input.parentNode.appendChild(preview)
          }
          preview.src = e.target.result
        }
        reader.readAsDataURL(file)
      }
    })
  })

  // Confirmation dialogs
  document.addEventListener("click", (e) => {
    if (e.target.classList.contains("confirm-delete") || e.target.closest(".confirm-delete")) {
      const element = e.target.classList.contains("confirm-delete") ? e.target : e.target.closest(".confirm-delete")
      const message = element.getAttribute("data-message") || "Are you sure you want to delete this item?"

      if (!confirm(message)) {
        e.preventDefault()
        return false
      }
    }
  })

  // Auto-save functionality for forms
  const autoSaveForms = document.querySelectorAll("[data-autosave]")
  autoSaveForms.forEach((form) => {
    const inputs = form.querySelectorAll("input, textarea, select")
    inputs.forEach((input) => {
      input.addEventListener(
        "input",
        debounce(() => {
          saveFormData(form)
        }, 1000),
      )
    })
  })

  // Copy to clipboard functionality
  document.addEventListener("click", (e) => {
    if (e.target.classList.contains("copy-btn") || e.target.closest(".copy-btn")) {
      e.preventDefault()
      const btn = e.target.classList.contains("copy-btn") ? e.target : e.target.closest(".copy-btn")
      const text = btn.getAttribute("data-copy") || btn.textContent

      navigator.clipboard.writeText(text).then(() => {
        const originalText = btn.innerHTML
        btn.innerHTML = '<i class="fas fa-check me-1"></i>Copied!'
        btn.classList.add("btn-success")

        setTimeout(() => {
          btn.innerHTML = originalText
          btn.classList.remove("btn-success")
        }, 2000)
      })
    }
  })
})

// Utility functions
function getCookie(name) {
  let cookieValue = null
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";")
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim()
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1))
        break
      }
    }
  }
  return cookieValue
}

function debounce(func, wait) {
  let timeout
  return function executedFunction(...args) {
    const later = () => {
      clearTimeout(timeout)
      func(...args)
    }
    clearTimeout(timeout)
    timeout = setTimeout(later, wait)
  }
}

function saveFormData(form) {
  const formData = new FormData(form)
  const data = {}
  for (const [key, value] of formData.entries()) {
    data[key] = value
  }
  localStorage.setItem(`form_${form.id}`, JSON.stringify(data))
}

function loadFormData(form) {
  const savedData = localStorage.getItem(`form_${form.id}`)
  if (savedData) {
    const data = JSON.parse(savedData)
    Object.keys(data).forEach((key) => {
      const input = form.querySelector(`[name="${key}"]`)
      if (input) {
        input.value = data[key]
      }
    })
  }
}

// Theme toggle functionality
function toggleTheme() {
  const body = document.body
  const isDark = body.classList.contains("dark-theme")

  if (isDark) {
    body.classList.remove("dark-theme")
    localStorage.setItem("theme", "light")
  } else {
    body.classList.add("dark-theme")
    localStorage.setItem("theme", "dark")
  }
}

// Load saved theme
const savedTheme = localStorage.getItem("theme")
if (savedTheme === "dark") {
  document.body.classList.add("dark-theme")
}

// Export functions for global use
window.TrackMyJourney = {
  getCookie,
  debounce,
  saveFormData,
  loadFormData,
  toggleTheme,
}
