// Import AOS library
import AOS from "aos"

// Initialize AOS (Animate On Scroll)
AOS.init({
  duration: 1000,
  once: true,
  offset: 100,
})

// Counter Animation
function animateCounters() {
  const counters = document.querySelectorAll(".counter")

  counters.forEach((counter) => {
    const target = Number.parseInt(counter.getAttribute("data-target"))
    const increment = target / 100
    let current = 0

    const updateCounter = () => {
      if (current < target) {
        current += increment
        counter.textContent = Math.floor(current).toLocaleString()
        requestAnimationFrame(updateCounter)
      } else {
        counter.textContent = target.toLocaleString()
      }
    }

    // Start animation when element is in view
    const observer = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          updateCounter()
          observer.unobserve(entry.target)
        }
      })
    })

    observer.observe(counter)
  })
}

// Smooth scrolling for navigation links
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

// Parallax effect for floating shapes
function parallaxEffect() {
  const shapes = document.querySelectorAll(".shape")
  const scrolled = window.pageYOffset
  const rate = scrolled * -0.5

  shapes.forEach((shape, index) => {
    const speed = (index + 1) * 0.1
    shape.style.transform = `translateY(${rate * speed}px)`
  })
}

// Throttled scroll event for performance
let ticking = false
function updateParallax() {
  if (!ticking) {
    requestAnimationFrame(() => {
      parallaxEffect()
      ticking = false
    })
    ticking = true
  }
}

window.addEventListener("scroll", updateParallax)

// Initialize animations when DOM is loaded
document.addEventListener("DOMContentLoaded", () => {
  animateCounters()

  // Add loading animation to cards
  const cards = document.querySelectorAll(".feature-card, .post-card, .impact-card")
  cards.forEach((card, index) => {
    card.style.animationDelay = `${index * 0.1}s`
    card.classList.add("fade-in")
  })

  // Trigger animations when cards come into view
  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.classList.add("visible")
      }
    })
  })

  cards.forEach((card) => observer.observe(card))
})

// Video placeholder click handler
document.querySelector(".play-button")?.addEventListener("click", () => {
  // Add your video play logic here
  console.log("Play button clicked")
})

// Contact form submission
document.querySelector(".contact-form")?.addEventListener("submit", function (e) {
  e.preventDefault()

  // Add loading state
  const submitBtn = this.querySelector('button[type="submit"]')
  const originalText = submitBtn.innerHTML
  submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Sending...'
  submitBtn.disabled = true

  // Simulate form submission (replace with actual AJAX call)
  setTimeout(() => {
    submitBtn.innerHTML = '<i class="fas fa-check me-2"></i>Sent!'
    setTimeout(() => {
      submitBtn.innerHTML = originalText
      submitBtn.disabled = false
      this.reset()
    }, 2000)
  }, 1500)
})

// Floating icons animation
document.querySelectorAll(".floating").forEach((icon, index) => {
  icon.addEventListener("mouseenter", function () {
    this.style.animationPlayState = "paused"
    this.style.transform = "scale(1.2) rotate(10deg)"
  })

  icon.addEventListener("mouseleave", function () {
    this.style.animationPlayState = "running"
    this.style.transform = ""
  })
})

// Posts slider auto-scroll (optional)
const postsSlider = document.querySelector(".posts-slider")
if (postsSlider) {
  let isScrolling = false

  postsSlider.addEventListener("mouseenter", () => {
    isScrolling = false
  })

  postsSlider.addEventListener("mouseleave", () => {
    isScrolling = true
  })

  // Auto-scroll functionality (uncomment if needed)
  /*
    setInterval(() => {
        if (isScrolling && postsSlider.scrollLeft < postsSlider.scrollWidth - postsSlider.clientWidth) {
            postsSlider.scrollLeft += 1;
        } else if (isScrolling) {
            postsSlider.scrollLeft = 0;
        }
    }, 50);
    */
}
