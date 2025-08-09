
  document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('.wishlist-button').forEach(button => {
      button.addEventListener('click', function () {
        const card = this.closest('.card');
        const title = card.dataset.title;
        const image = card.dataset.image;
        const price = card.dataset.price;

        // Create and submit a hidden form
        const form = document.createElement('form');
        form.method = 'POST';
        form.action = '/add_to_wishlist';

        const inputTitle = document.createElement('input');
        inputTitle.type = 'hidden';
        inputTitle.name = 'card_title';
        inputTitle.value = title;

        const inputImage = document.createElement('input');
        inputImage.type = 'hidden';
        inputImage.name = 'image_url';
        inputImage.value = image;

        const inputPrice = document.createElement('input');
        inputPrice.type = 'hidden';
        inputPrice.name = 'price';
        inputPrice.value = price;

        form.appendChild(inputTitle);
        form.appendChild(inputImage);
        form.appendChild(inputPrice);
        document.body.appendChild(form);
        form.submit();
      });
    });
  });