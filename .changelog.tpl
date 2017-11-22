{{#general_title}}
# {{{title}}}


{{/general_title}}
{{#versions}}
## [{{{label}}}](https://github.com/BBVA/data-refinery/tree/{{{tag}}})

{{#sections}}
### {{{label}}}

{{#commits}}
* [{{{commit.sha1_short}}}](https://github.com/BBVA/data-refinery/commit/{{{commit.sha1}}}) {{{subject}}}
{{#body}}

{{{body_indented}}}
{{/body}}

{{/commits}}
{{/sections}}

{{/versions}}