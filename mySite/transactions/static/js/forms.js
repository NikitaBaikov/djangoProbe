// $ - синоним функции jQuery
	
// type задает имя в html-шаблоне
// selector указывает на последнюю форму в списке
// Данные о количестве форм берутся из management_form в django
// Создаем копию последней формы (определяется через selector)
// Вручную переименовываем input'ы и label'ы формы, сбрасываем значения
// Перезаписываем счетчик форм
// Добавляем в конец
function addForm(selector, type) {
	var newElement = $(selector).clone(true);
	var total = $('#id_' + type + '-TOTAL_FORMS').val();

	newElement.find(':input').each(function() {
		var name = $(this).attr('name').replace('-' + (total-1) + '-','-' + total + '-');
		var id = 'id_' + name;
		$(this).attr({'name': name, 'id': id}).val('').removeAttr('checked');
		});

	newElement.find('label').each(function() {
		var newFor = $(this).attr('for').replace('-' + (total-1) + '-','-' + total + '-');
		$(this).attr('for', newFor);
		});
	total++;
	$('#id_' + type + '-TOTAL_FORMS').val(total);
	$(selector).after(newElement);
	}

// Пересчет количества форм
// type задает имя в html-шаблоне
// Данные о количестве форм берутся из management_form в django
function numberOfForms (type) {
	var total = $('#id_' + type + '-TOTAL_FORMS').val();
	return total;
}

function deleteForm (btn, type, rtype) {
	var formCount = numberOfForms (type);
	if (formCount > 1) {
		$(btn).parents(rtype).remove();
		var forms = $(rtype); 
		$('#id_' + type + '-TOTAL_FORMS').val(forms.length);
		var i = 0;

		// TODO

		for (formCount = forms.length; i < formCount; i++) {
			$(forms.get(i)).children().children().each(function () {
					if ($(this).attr('type') == 'text') updateElementIndex(this, prefix, i);
					});
	} 
	else {
		alert("Должна быть хотя бы одна форма товара!");
	}
	return false;
}

