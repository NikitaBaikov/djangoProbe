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

// Удаляет форму, если их как минимум несколько
// Похоже на добавление
// btn - указывает на кнопку, которую нажимаем для удаления
// type - имя в html шаблоне на добавление 
// rtype - имя в html шаблоне на удаление
function deleteForm(btn, type, rtype) {
	var fl = numberOfForms (type);

	if (fl < 2) {
		alert("Должна быть хотя бы одна форма для товара!");
		return false;
	}	

	$(btn).parents(rtype).remove();
	var forms = $(rtype);
	$('#id_' + type + '-TOTAL_FORMS').val(fl-1);
	
	for (var i=0, formCount=forms.length; i<formCount; i++) {
		$(forms.get(i)).find(":input").each(function() {
			var re = new RegExp(type+'-\\d+');
            var name = $(this).attr('name').replace(re, type+'-'+i);
            var id = 'id_' + name;
            $(this).attr({'name': name, 'id' : id});
            });

		$(forms.get(i)).find("label").each(function() {
			var re = new RegExp(type+'-\\d+');
            var newFor = $(this).attr('for').replace(re, type+'-'+i);
            $(this).attr('for', newFor);
            });

	}
	return true;
}



