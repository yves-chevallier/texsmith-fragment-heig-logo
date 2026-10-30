{# The logo on the first page, from the sheet's top-left corner, and the
   content moved below it. #}
{% set logo %}year: "{{ heiglogo_year }}"{% if heiglogo_color %}, color: true{% endif %}{% if heiglogo_group %}, group: "{{ heiglogo_group }}"{% endif %}{% endset %}
#set page(background: heiglogo-page(left: {{ heiglogo_typst_left }}, top: {{ heiglogo_typst_top }}, {{ logo }}))
#heiglogo-clearance(top: {{ heiglogo_typst_top }}, {{ logo }})
