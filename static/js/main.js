// Функция для загрузки валют из сервера
async function loadCurrencies() {
    try {
      const response = await fetch('/currencies');
      const data = await response.json();
      if (data.currencies) {
        // Заполняем выпадающий список валют
        const fromCurrencySelect = document.getElementById('fromCurrency');
        const toCurrencySelect = document.getElementById('toCurrency');
        
        data.currencies.forEach(currency => {
          const fromOption = document.createElement('option');
          fromOption.value = currency;
          fromOption.textContent = currency;
          fromCurrencySelect.appendChild(fromOption);
  
          const toOption = document.createElement('option');
          toOption.value = currency;
          toOption.textContent = currency;
          toCurrencySelect.appendChild(toOption);
        });
      }
    } catch (error) {
      console.error("Error loading currencies:", error);
    }
  }
  
  // Функция для обновления времени последнего обновления
  async function updateLastUpdated() {
    try {
      const response = await fetch('/last-update');
      const data = await response.json();
      if (data.last_update) {
        document.getElementById('lastUpdated').innerText = `Последнее обновление: ${data.last_update}`;
      }
    } catch (error) {
      console.error('Error fetching last updated time:', error);
    }
  }
  
  // Функция для конвертации валюты
  document.getElementById('convertButton').addEventListener('click', async function () {
    const fromCurrency = document.getElementById('fromCurrency').value;
    const toCurrency = document.getElementById('toCurrency').value;
    const amount = document.getElementById('amount').value;
  
    if (!fromCurrency || !toCurrency || !amount) {
      document.getElementById('conversionResult').innerText = 'Пожалуйста, заполните все поля';
      return;
    }
  
    const response = await fetch('/convert', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        from: fromCurrency,
        to: toCurrency,
        amount: amount
      })
    });
  
    const data = await response.json();
  
    if (data.result) {
      document.getElementById('conversionResult').innerText = `${data.result} ${toCurrency}`;
    } else {
      document.getElementById('conversionResult').innerText = 'Ошибка при конвертации';
    }
  
    // Обновляем время последнего обновления
    updateLastUpdated();
  });
  
  // Загружаем валюты при загрузке страницы
  window.onload = function() {
    loadCurrencies();
    updateLastUpdated();
  };
  