function showRescheduleForm(appointmentId) {
    document.getElementById('reschedule_appointment_id').value = appointmentId;
    document.getElementById('rescheduleModal').style.display = 'block';
}

function hideRescheduleForm() {
    document.getElementById('rescheduleModal').style.display = 'none';
}

function updateAvailableTimes() {
    const dateInput = document.getElementById('new_date');
    const timeSelect = document.getElementById('new_time');
    const appointmentId = document.getElementById('reschedule_appointment_id').value;
    
    if (!dateInput.value) {
        timeSelect.innerHTML = '<option value="">Сначала выберите дату</option>';
        return;
    }
    
    // Очищаем текущие опции
    timeSelect.innerHTML = '<option value="">Загрузка...</option>';
    
    // Отправляем AJAX запрос для получения доступных временных слотов
    fetch(`/profile/get-available-times/?date=${dateInput.value}&appointment_id=${appointmentId}`)
        .then(response => response.json())
        .then(data => {
            timeSelect.innerHTML = '<option value="">Выберите время</option>';
            if (data.available_times && data.available_times.length > 0) {
                data.available_times.forEach(time => {
                    const option = document.createElement('option');
                    option.value = time;
                    option.textContent = time;
                    timeSelect.appendChild(option);
                });
            } else {
                timeSelect.innerHTML = '<option value="">Нет доступного времени</option>';
            }
        })
        .catch(error => {
            console.error('Ошибка при получении доступного времени:', error);
            timeSelect.innerHTML = '<option value="">Ошибка загрузки</option>';
        });
}