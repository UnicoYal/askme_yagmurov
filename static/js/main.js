function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let i = 0; i < cookies.length; i++) {
          const cookie = cookies[i].trim();
          // Does this cookie string begin with the name we want?
          if (cookie.substring(0, name.length + 1) === (name + '=')) {
              cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
              break;
          }
      }
  }
  return cookieValue;
}

const likeSections = document.getElementsByClassName('like-section')

for (const section of likeSections) {
  const [likeButton, dislikeButton, _, counter] = section.children

  likeButton.addEventListener('click', () => {
    const request = new Request(`/set_mark/`, {
      method: 'post',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCookie('csrftoken'),
      },
      body: JSON.stringify({
        item_id: likeButton.dataset.id,
        item_type: likeButton.dataset.type,
        operation_type: 'like',
      })
    })

    fetch(request)
      .then((response) => response.json())
      .then((data) => {
        counter.innerHTML = data.likes_count;
        likeButton.disabled = true;
        dislikeButton.disabled = true;
      })
  })

  dislikeButton.addEventListener('click', () => {
    const request = new Request(`/set_mark/`, {
      method: 'post',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCookie('csrftoken'),
      },
      body: JSON.stringify({
        item_id: dislikeButton.dataset.id,
        item_type: dislikeButton.dataset.type,
        operation_type: 'dislike',
      })
    })

    fetch(request)
      .then((response) => response.json())
      .then((data) => {
        counter.innerHTML = data.likes_count;
        likeButton.disabled = true;
        dislikeButton.disabled = true;
      })
  })
}

const rightAnswerSections = document.getElementsByClassName('form-check')

for(const section of rightAnswerSections) {
  const [selector] = section.children
  selector.addEventListener('click', () => {
    const request = new Request('/correct_answer/', {
      method: 'post',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCookie('csrftoken'),
      },
      body: JSON.stringify({
        answer_id: selector.dataset.id
      })
    })

    fetch(request)
    .then((response) => response.json())
    .then((data) => {
      selector.checked = data.correct;
    })
  })
}

document.addEventListener('DOMContentLoaded', function() {
  for(section of likeSections) {
    const [likeButton, dislikeButton] = section.children
    const request = new Request(`/check_mark/`, {
      method: 'post',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCookie('csrftoken'),
      },
      body: JSON.stringify({
        item_id: likeButton.dataset.id,
        user_id: likeButton.dataset.user,
        item_type: likeButton.dataset.type,
      })
    })

    fetch(request)
      .then((response) => response.json())
      .then((data) => {
        likeButton.disabled = data.is_marked;
        dislikeButton.disabled = data.is_marked;
      })
  }

  for(section of rightAnswerSections) {
    const [selector] = section.children
    const request = new Request('/check_answer/', {
      method: 'post',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCookie('csrftoken'),
      },
      body: JSON.stringify({
        answer_id: selector.dataset.id
      })
    })

    fetch(request)
    .then((response) => response.json())
    .then((data) => {
      selector.checked = data.is_correct;
      selector.disabled = !data.is_question_author;
    })
  }
});
