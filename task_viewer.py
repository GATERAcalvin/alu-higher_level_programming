#!/usr/bin/env python3
"""task_viewer.py - run the tasks in this repo and see the results in your browser.

Usage (from the repo root):   python task_viewer.py
Then open http://127.0.0.1:8765 (it opens automatically).

It only listens on your own computer (127.0.0.1) and only runs files that
live in the python-* project folders next to this script.
"""
import ast
import json
import os
import re
import secrets
import shutil
import subprocess
import sys
import threading
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

ROOT = os.path.dirname(os.path.abspath(__file__))
TOKEN = secrets.token_hex(16)
TESTS = json.loads(r'''{
 "python-if_else_loops_functions/7-islower.py": "islower = __import__('7-islower').islower\nfor c in \"aHA3g\":\n    print(\"{} is {}\".format(c, \"lower\" if islower(c) else \"upper\"))\n",
 "python-if_else_loops_functions/8-uppercase.py": "uppercase = __import__('8-uppercase').uppercase\nuppercase(\"best\")\nuppercase(\"Best School 98 Battery street\")\n",
 "python-if_else_loops_functions/9-print_last_digit.py": "print_last_digit = __import__('9-print_last_digit').print_last_digit\nprint_last_digit(98)\nprint_last_digit(0)\nr = print_last_digit(-1024)\nprint(r)\n",
 "python-if_else_loops_functions/10-add.py": "add = __import__('10-add').add\nprint(add(1, 2))\nprint(add(98, 0))\nprint(add(100, -2))\n",
 "python-if_else_loops_functions/11-pow.py": "pow = __import__('11-pow').pow\nprint(pow(2, 2))\nprint(pow(98, 2))\nprint(pow(98, 0))\nprint(pow(100, -2))\nprint(pow(-4, 5))\n",
 "python-if_else_loops_functions/12-fizzbuzz.py": "fizzbuzz = __import__('12-fizzbuzz').fizzbuzz\nfizzbuzz()\nprint(\"\")\n",
 "python-data_structures/0-print_list_integer.py": "print_list_integer = __import__('0-print_list_integer').print_list_integer\nprint_list_integer([1, 2, 3, 4, 5])\n",
 "python-data_structures/1-element_at.py": "element_at = __import__('1-element_at').element_at\nmy_list = [1, 2, 3, 4, 5]\nidx = 3\nprint(\"Element at index {:d} is {}\".format(idx, element_at(my_list, idx)))\n",
 "python-data_structures/2-replace_in_list.py": "replace_in_list = __import__('2-replace_in_list').replace_in_list\nmy_list = [1, 2, 3, 4, 5]\nnew_list = replace_in_list(my_list, 3, 9)\nprint(new_list)\nprint(my_list)\n",
 "python-data_structures/4-new_in_list.py": "new_in_list = __import__('4-new_in_list').new_in_list\nmy_list = [1, 2, 3, 4, 5]\nnew_list = new_in_list(my_list, 3, 9)\nprint(new_list)\nprint(my_list)\n",
 "python-data_structures/5-no_c.py": "no_c = __import__('5-no_c').no_c\nprint(no_c(\"Best School\"))\nprint(no_c(\"Chicago\"))\nprint(no_c(\"C is fun!\"))\n",
 "python-data_structures/6-print_matrix_integer.py": "print_matrix_integer = __import__('6-print_matrix_integer').print_matrix_integer\nmatrix = [\n    [1, 2, 3],\n    [4, 5, 6],\n    [7, 8, 9]\n]\n\nprint_matrix_integer(matrix)\nprint(\"--\")\nprint_matrix_integer()\n",
 "python-data_structures/7-add_tuple.py": "add_tuple = __import__('7-add_tuple').add_tuple\ntuple_a = (1, 89)\ntuple_b = (88, 11)\nprint(add_tuple(tuple_a, tuple_b))\nprint(add_tuple(tuple_a, (1, )))\nprint(add_tuple(tuple_a, ()))\n",
 "python-data_structures/8-multiple_returns.py": "multiple_returns = __import__('8-multiple_returns').multiple_returns\nsentence = \"At school, I learnt C!\"\nlength, first = multiple_returns(sentence)\nprint(\"Length: {:d} - First character: {}\".format(length, first))\n",
 "python-data_structures/9-max_integer.py": "max_integer = __import__('9-max_integer').max_integer\nmy_list = [1, 90, 2, 13, 34, 5, -13, 3]\nprint(\"Max: {}\".format(max_integer(my_list)))\n",
 "python-data_structures/10-divisible_by_2.py": "divisible_by_2 = __import__('10-divisible_by_2').divisible_by_2\nmy_list = [0, 1, 2, 3, 4, 5, 6]\nlist_result = divisible_by_2(my_list)\n\ni = 0\nwhile i < len(list_result):\n    print(\"{:d} {:s} divisible by 2\".format(my_list[i], \"is\" if list_result[i] else \"is not\"))\n    i += 1\n",
 "python-data_structures/11-delete_at.py": "delete_at = __import__('11-delete_at').delete_at\nmy_list = [1, 2, 3, 4, 5]\nnew_list = delete_at(my_list, 3)\nprint(new_list)\nprint(my_list)\n",
 "python-more_data_structures/0-square_matrix_simple.py": "square_matrix_simple = __import__('0-square_matrix_simple').square_matrix_simple\nmatrix = [\n    [1, 2, 3],\n    [4, 5, 6],\n    [7, 8, 9]\n]\n\nnew_matrix = square_matrix_simple(matrix)\nprint(new_matrix)\nprint(matrix)\n",
 "python-more_data_structures/1-search_replace.py": "search_replace = __import__('1-search_replace').search_replace\nmy_list = [1, 2, 3, 4, 5, 4, 2, 1, 1, 4, 89]\nnew_list = search_replace(my_list, 2, 89)\n\nprint(new_list)\nprint(my_list)\n",
 "python-more_data_structures/2-uniq_add.py": "uniq_add = __import__('2-uniq_add').uniq_add\nmy_list = [1, 2, 3, 1, 4, 2, 5]\nresult = uniq_add(my_list)\nprint(\"Result: {:d}\".format(result))\n",
 "python-more_data_structures/4-only_diff_elements.py": "only_diff_elements = __import__('4-only_diff_elements').only_diff_elements\nset_1 = { \"Python\", \"C\", \"Javascript\" }\nset_2 = { \"Bash\", \"C\", \"Ruby\", \"Perl\" }\nod_set = only_diff_elements(set_1, set_2)\nprint(sorted(list(od_set)))\n",
 "python-more_data_structures/5-number_keys.py": "number_keys = __import__('5-number_keys').number_keys\na_dictionary = { 'language': \"C\", 'number': 13, 'track': \"Low level\" }\nnb_keys = number_keys(a_dictionary)\nprint(\"Number of keys: {:d}\".format(nb_keys))\n",
 "python-more_data_structures/6-print_sorted_dictionary.py": "print_sorted_dictionary = __import__('6-print_sorted_dictionary').print_sorted_dictionary\na_dictionary = { 'language': \"C\", 'Number': 89, 'track': \"Low level\", 'ids': [1, 2, 3] }\nprint_sorted_dictionary(a_dictionary)\n",
 "python-more_data_structures/7-update_dictionary.py": "update_dictionary = __import__('7-update_dictionary').update_dictionary\nprint_sorted_dictionary = __import__('6-print_sorted_dictionary').print_sorted_dictionary\na_dictionary = { 'language': \"C\", 'number': 89, 'track': \"Low level\" }\nnew_dict = update_dictionary(a_dictionary, 'language', \"Python\")\nprint_sorted_dictionary(new_dict)\nprint(\"--\")\nprint_sorted_dictionary(a_dictionary)\n\nprint(\"--\")\nprint(\"--\")\n\nnew_dict = update_dictionary(a_dictionary, 'city', \"San Francisco\")\nprint_sorted_dictionary(new_dict)\nprint(\"--\")\nprint_sorted_dictionary(a_dictionary)\n",
 "python-more_data_structures/8-simple_delete.py": "simple_delete = __import__('8-simple_delete').simple_delete\nprint_sorted_dictionary = __import__('6-print_sorted_dictionary').print_sorted_dictionary\na_dictionary = { 'language': \"C\", 'Number': 89, 'track': \"Low\", 'ids': [1, 2, 3] }\nnew_dict = simple_delete(a_dictionary, 'track')\nprint_sorted_dictionary(a_dictionary)\nprint(\"--\")\nprint_sorted_dictionary(new_dict)\n\nprint(\"--\")\nprint(\"--\")\nnew_dict = simple_delete(a_dictionary, 'c_is_fun')\nprint_sorted_dictionary(a_dictionary)\nprint(\"--\")\nprint_sorted_dictionary(new_dict)\n",
 "python-more_data_structures/9-multiply_by_2.py": "multiply_by_2 = __import__('9-multiply_by_2').multiply_by_2\nprint_sorted_dictionary = __import__('6-print_sorted_dictionary').print_sorted_dictionary\na_dictionary = {'John': 12, 'Alex': 8, 'Bob': 14, 'Mike': 14, 'Molly': 16}\nnew_dict = multiply_by_2(a_dictionary)\nprint_sorted_dictionary(a_dictionary)\nprint(\"--\")\nprint_sorted_dictionary(new_dict)\n",
 "python-more_data_structures/10-best_score.py": "best_score = __import__('10-best_score').best_score\na_dictionary = {'John': 12, 'Bob': 14, 'Mike': 14, 'Molly': 16, 'Adam': 10}\nbest_key = best_score(a_dictionary)\nprint(\"Best score: {}\".format(best_key))\n\nbest_key = best_score(None)\nprint(\"Best score: {}\".format(best_key))\n",
 "python-more_data_structures/11-multiply_list_map.py": "multiply_list_map = __import__('11-multiply_list_map').multiply_list_map\nmy_list = [1, 2, 3, 4, 6]\nnew_list = multiply_list_map(my_list, 4)\nprint(new_list)\nprint(my_list)\n",
 "python-more_data_structures/12-roman_to_int.py": "roman_to_int = __import__('12-roman_to_int').roman_to_int\nfor roman_number in [\"X\", \"VII\", \"IX\", \"LXXXVII\", \"DCCVII\"]:\n    print(\"{} = {}\".format(roman_number, roman_to_int(roman_number)))\n",
 "python-exceptions/0-safe_print_list.py": "safe_print_list = __import__('0-safe_print_list').safe_print_list\nmy_list = [1, 2, 3, 4, 5]\n\nnb_print = safe_print_list(my_list, 2)\nprint(\"nb_print: {:d}\".format(nb_print))\nnb_print = safe_print_list(my_list, len(my_list))\nprint(\"nb_print: {:d}\".format(nb_print))\nnb_print = safe_print_list(my_list, len(my_list) + 2)\nprint(\"nb_print: {:d}\".format(nb_print))\n",
 "python-exceptions/1-safe_print_integer.py": "safe_print_integer = __import__('1-safe_print_integer').safe_print_integer\nfor value in (89, -89, \"School\"):\n    if not safe_print_integer(value):\n        print(\"{} is not an integer\".format(value))\n",
 "python-exceptions/2-safe_print_list_integers.py": "safe_print_list_integers = __import__('2-safe_print_list_integers').safe_print_list_integers\nmy_list = [1, 2, 3, 4, 5]\n\nnb_print = safe_print_list_integers(my_list, 2)\nprint(\"nb_print: {:d}\".format(nb_print))\n\nmy_list = [1, 2, 3, \"School\", 4, 5, [1, 2, 3]]\nnb_print = safe_print_list_integers(my_list, len(my_list))\nprint(\"nb_print: {:d}\".format(nb_print))\n\ntry:\n    safe_print_list_integers(my_list, len(my_list) + 2)\nexcept IndexError as e:\n    print(\"\\nIndexError: {}\".format(e))\n",
 "python-exceptions/4-list_division.py": "list_division = __import__('4-list_division').list_division\nmy_l_1 = [10, 8, 4]\nmy_l_2 = [2, 4, 4]\nprint(list_division(my_l_1, my_l_2, max(len(my_l_1), len(my_l_2))))\n\nprint(\"--\")\n\nmy_l_1 = [10, 8, 4, 4]\nmy_l_2 = [2, 0, \"H\", 2, 7]\nprint(list_division(my_l_1, my_l_2, max(len(my_l_1), len(my_l_2))))\n",
 "python-exceptions/5-raise_exception.py": "raise_exception = __import__('5-raise_exception').raise_exception\ntry:\n    raise_exception()\nexcept TypeError as te:\n    print(\"Exception raised\")\n",
 "python-exceptions/6-raise_exception_msg.py": "raise_exception_msg = __import__('6-raise_exception_msg').raise_exception_msg\ntry:\n    raise_exception_msg(\"C is fun\")\nexcept NameError as ne:\n    print(ne)\n",
 "python-exceptions/100-safe_print_integer_err.py": "safe_print_integer_err = __import__('100-safe_print_integer_err').safe_print_integer_err\nfor value in (89, -89, \"School\"):\n    if not safe_print_integer_err(value):\n        print(\"{} is not an integer\".format(value))\n",
 "python-exceptions/101-safe_function.py": "safe_function = __import__('101-safe_function').safe_function\ndef my_div(a, b):\n    return a / b\n\n\nresult = safe_function(my_div, 10, 2)\nprint(\"result of my_div: {}\".format(result))\n\nresult = safe_function(my_div, 10, 0)\nprint(\"result of my_div: {}\".format(result))\n\n\ndef print_list(my_list, len):\n    i = 0\n    while i < len:\n        print(my_list[i])\n        i += 1\n    return len\n\n\nresult = safe_function(print_list, [1, 2, 3, 4], 10)\nprint(\"result of print_list: {}\".format(result))\n",
 "python-exceptions/102-magic_calculation.py": "magic_calculation = __import__('102-magic_calculation').magic_calculation\nprint(magic_calculation(3, 2))\nprint(magic_calculation(1, 5))\nprint(magic_calculation(0, 4))\n"
}''')
HTML = r'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>ALU Task Runner</title>
<style>

/* Layout: sticky project tabs over a list of task rows; each row pairs the source with the real captured output. */
:root{
  --bg:#f5f7f6; --surface:#ffffff; --fg:#14201c; --muted:#5a6a63; --line:#d9e1dd;
  --accent:#0b7a62; --accent-soft:#dcf1ea; --warn:#9a5b00; --warn-soft:#fbefd5; --bad:#b3261e;
  --term-bg:#101a17; --term-fg:#d6efe6; --term-dim:#7fa196; --code-bg:#eef2f0; --code-fg:#1b2a25;
  --display:"Space Grotesk",system-ui,sans-serif; --body:"Inter",system-ui,sans-serif; --mono:"JetBrains Mono",ui-monospace,Menlo,Consolas,monospace;
}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){
  --bg:#0d1512; --surface:#14201c; --fg:#e4f0ea; --muted:#8fa69c; --line:#26362f;
  --accent:#4fd1ae; --accent-soft:#17352c; --warn:#f0c168; --warn-soft:#3a2f14; --bad:#ff8a80;
  --term-bg:#08100d; --term-fg:#d6efe6; --term-dim:#6f9186; --code-bg:#0f1a16; --code-fg:#cfe3da; color-scheme:dark}}
:root[data-theme="dark"]{
  --bg:#0d1512; --surface:#14201c; --fg:#e4f0ea; --muted:#8fa69c; --line:#26362f;
  --accent:#4fd1ae; --accent-soft:#17352c; --warn:#f0c168; --warn-soft:#3a2f14; --bad:#ff8a80;
  --term-bg:#08100d; --term-fg:#d6efe6; --term-dim:#6f9186; --code-bg:#0f1a16; --code-fg:#cfe3da; color-scheme:dark}
body{background:var(--bg);color:var(--fg);font:15px/1.5 var(--body);padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px));padding-block:0 48px}
body::before{content:"";position:fixed;inset:0 0 auto;height:env(safe-area-inset-top,0px);z-index:10;background:var(--bg)}
.wrap{max-width:1120px;margin:0 auto}
header{padding-block:28px 8px}
h1{font:700 clamp(26px,4vw,36px)/1.15 var(--display);margin:0 0 6px;text-wrap:balance;letter-spacing:-.01em}
.sub{color:var(--muted);margin:0;max-width:62ch}
.stats{display:flex;flex-wrap:wrap;gap:8px 20px;margin:16px 0 0;font-size:13px;color:var(--muted)}
.stats b{color:var(--fg);font-variant-numeric:tabular-nums}
nav{position:sticky;top:env(safe-area-inset-top,0px);z-index:5;background:var(--bg);padding-block:12px;border-bottom:1px solid var(--line);margin-top:12px}
.tabs{display:flex;gap:8px;overflow-x:auto;scrollbar-width:thin}
.tab{flex:none;appearance:none;border:1px solid var(--line);background:var(--surface);color:var(--fg);font:500 13px var(--body);padding:8px 12px;border-radius:6px;cursor:pointer;display:flex;gap:8px;align-items:center}
.tab span{color:var(--muted);font-variant-numeric:tabular-nums}
.tab[aria-selected="true"]{background:var(--accent);border-color:var(--accent);color:#fff}
.tab[aria-selected="true"] span{color:#d8f5ec}
.tab:focus-visible,.copy:focus-visible,summary:focus-visible{outline:2px solid var(--accent);outline-offset:2px}
.dirline{display:flex;flex-wrap:wrap;justify-content:space-between;gap:6px 16px;align-items:baseline;margin:22px 0 14px}
.dirline h2{font:700 22px var(--display);margin:0}
.dirline code{font:12px var(--mono);color:var(--muted)}
.list{display:flex;flex-direction:column;gap:18px}
.task{background:var(--surface);border:1px solid var(--line);border-radius:8px;overflow:hidden}
.thead{display:flex;flex-wrap:wrap;gap:6px 12px;align-items:center;padding:12px 16px;border-bottom:1px solid var(--line)}
.thead h3{font:600 15px var(--body);margin:0;flex:1 1 220px;min-width:0}
.file{font:12px var(--mono);color:var(--muted)}
.chip{font:600 11px var(--body);letter-spacing:.04em;text-transform:uppercase;padding:3px 8px;border-radius:4px;background:var(--accent-soft);color:var(--accent)}
.chip.sample{background:var(--warn-soft);color:var(--warn)}
.chip.bad{background:var(--warn-soft);color:var(--bad)}
.panes{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr)}
@media (max-width:760px){.panes{grid-template-columns:minmax(0,1fr)}}
.pane{min-width:0;display:flex;flex-direction:column}
.pane+.pane{border-left:1px solid var(--line)}
@media (max-width:760px){.pane+.pane{border-left:0;border-top:1px solid var(--line)}}
.label{display:flex;justify-content:space-between;align-items:center;font:600 11px var(--body);letter-spacing:.06em;text-transform:uppercase;color:var(--muted);padding:8px 16px 0}
.copy{font:500 11px var(--body);background:none;border:1px solid var(--line);color:var(--muted);border-radius:4px;padding:2px 8px;cursor:pointer}
pre{margin:8px 0 0;padding:8px 16px 16px;font:13px/1.55 var(--mono);overflow-x:auto;flex:1;white-space:pre}
pre.code{color:var(--code-fg);background:var(--code-bg);margin-top:8px}
.term{background:var(--term-bg);flex:1;display:flex;flex-direction:column}
.term .label{color:var(--term-dim)}
.term pre{color:var(--term-fg);max-height:340px;overflow:auto}
.term .cmd{color:var(--term-dim)}
.term .err{color:#f0c168}
details.used{border-top:1px solid var(--line)}
summary{cursor:pointer;font:500 12.5px var(--body);color:var(--muted);padding:8px 16px}
.note{padding:8px 16px;font-size:12.5px;color:var(--muted);border-top:1px solid var(--line)}
.empty{color:var(--term-dim);font-style:italic}
footer{margin-top:32px;color:var(--muted);font-size:12.5px;max-width:70ch}
@media (prefers-reduced-motion:no-preference){.task{transition:border-color .15s}.task:hover{border-color:var(--accent)}}

.runrow{display:flex;flex-wrap:wrap;gap:8px;align-items:center;padding:10px 16px;border-top:1px solid var(--line)}
.runrow input,.runrow textarea{font:13px var(--mono);background:var(--code-bg);color:var(--code-fg);border:1px solid var(--line);border-radius:6px;padding:6px 8px;min-width:0}
.runrow input{flex:1 1 180px}
.btn{appearance:none;border:0;background:var(--accent);color:#fff;font:600 13px var(--body);padding:8px 14px;border-radius:6px;cursor:pointer}
.btn.ghost{background:none;border:1px solid var(--line);color:var(--fg)}
.btn:disabled{opacity:.6;cursor:progress}
textarea.test{width:100%;min-height:110px;resize:vertical;font:13px/1.5 var(--mono);background:var(--code-bg);color:var(--code-fg);border:0;border-top:1px solid var(--line);padding:10px 16px;display:block}
.bar{display:flex;flex-wrap:wrap;gap:8px;align-items:center;margin:0 0 14px}
.exit{font:12px var(--mono);color:var(--term-dim);padding:0 16px 10px}
.term pre{min-height:60px}
.banner{background:var(--warn-soft);color:var(--warn);padding:10px 14px;border-radius:6px;margin:16px 0;font-size:13.5px}
</style></head><body>
<div class="wrap">
<header>
  <h1>ALU Task Runner</h1>
  <p class="sub">Runs the real files in your clone and shows what they print. Edit the test box on a function task and run it again.</p>
</header>
<nav><div class="tabs" id="tabs" role="tablist"></div></nav>
<main id="view"></main>
</div>
<script>
var TOKEN = "__TOKEN__";
(function(){
  var tabs = document.getElementById('tabs'), view = document.getElementById('view'), D = [];
  function el(t, c, x){ var e = document.createElement(t); if(c) e.className = c; if(x != null) e.textContent = x; return e; }
  function nice(d){ return d.replace(/^python-/, '').replace(/_/g, ' ').replace(/\b\w/g, function(c){ return c.toUpperCase(); }); }
  function post(body){
    return fetch('/api/run', {method: 'POST', headers: {'Content-Type': 'application/json', 'X-Token': TOKEN}, body: JSON.stringify(body)}).then(function(r){ return r.json(); });
  }
  function show(pre, ex, r){
    pre.textContent = '';
    if(r.error){ pre.appendChild(el('span', 'err', r.error)); ex.textContent = ''; return; }
    if(r.stdout){ pre.appendChild(document.createTextNode(r.stdout)); }
    if(r.stderr){ pre.appendChild(el('span', 'err', (r.stdout && !/\n$/.test(r.stdout) ? '\n' : '') + r.stderr)); }
    if(!r.stdout && !r.stderr){ pre.appendChild(el('span', 'empty', '(no output)')); }
    ex.textContent = 'exit code ' + r.code;
  }
  function card(dir, i){
    var t = el('article', 'task'), th = el('div', 'thead');
    th.appendChild(el('h3', null, i.file));
    th.appendChild(el('span', 'chip sample', i.kind === 'function' ? 'function file' : (i.kind === 'shell' ? 'shell script' : 'script')));
    t.appendChild(th);
    var pn = el('div', 'panes'), p1 = el('div', 'pane'), l1 = el('div', 'label'); l1.appendChild(el('span', null, 'Source'));
    var code = el('pre', 'code'); code.textContent = i.source; code.tabIndex = 0; p1.appendChild(l1); p1.appendChild(code);
    var p2 = el('div', 'pane term'), l2 = el('div', 'label'); l2.appendChild(el('span', null, 'Output'));
    var out = el('pre'); out.appendChild(el('span', 'empty', 'Press Run to see the output.')); out.tabIndex = 0;
    var ex = el('div', 'exit'); p2.appendChild(l2); p2.appendChild(out); p2.appendChild(ex);
    pn.appendChild(p1); pn.appendChild(p2); t.appendChild(pn);
    var ta = null, args = null, e1 = null, e2 = null;
    if(i.kind === 'function'){
      ta = el('textarea', 'test'); ta.value = i.test; ta.spellcheck = false; ta.setAttribute('aria-label', 'Test code for ' + i.file); t.appendChild(ta);
    }
    var row = el('div', 'runrow');
    if(i.kind === 'script'){ args = el('input'); args.placeholder = 'Arguments, e.g. 79 10 -40'; args.setAttribute('aria-label', 'Arguments'); row.appendChild(args); }
    if(i.kind === 'shell'){
      e1 = el('input'); e2 = el('input');
      if(i.file === '0-run'){ e1.placeholder = 'PYFILE, e.g. main.py'; row.appendChild(e1); }
      else { e2.placeholder = "PYCODE, e.g. print(1+2)"; row.appendChild(e2); }
    }
    var btn = el('button', 'btn', 'Run'); btn.type = 'button';
    btn.addEventListener('click', function(){ return go(); });
    row.appendChild(btn); t.appendChild(row);
    function go(){
      btn.disabled = true; btn.textContent = 'Running...';
      return post({dir: dir, file: i.file, args: args ? args.value : '', code: ta ? ta.value : '', PYFILE: e1 ? e1.value : '', PYCODE: e2 ? e2.value : ''})
        .then(function(r){ show(out, ex, r); }, function(){ show(out, ex, {error: 'Could not reach the viewer. Is it still running in your terminal?'}); })
        .then(function(){ btn.disabled = false; btn.textContent = 'Run'; });
    }
    t.run = go; t.needsInput = (i.kind === 'shell');
    return t;
  }
  function render(slug){
    var p = D.filter(function(x){ return x.dir === slug; })[0] || D[0];
    if(!p){ view.appendChild(el('div', 'banner', 'No python-* project folders found next to task_viewer.py.')); return; }
    Array.prototype.forEach.call(tabs.children, function(b){ b.setAttribute('aria-selected', b.dataset.dir === p.dir ? 'true' : 'false'); });
    view.innerHTML = '';
    var h = el('div', 'dirline'); h.appendChild(el('h2', null, nice(p.dir))); h.appendChild(el('code', null, p.dir + '/')); view.appendChild(h);
    var bar = el('div', 'bar'), all = el('button', 'btn', 'Run every task in this project'); all.type = 'button';
    bar.appendChild(all); view.appendChild(bar);
    var list = el('div', 'list'), cards = p.items.map(function(i){ return card(p.dir, i); });
    cards.forEach(function(c){ list.appendChild(c); }); view.appendChild(list);
    all.addEventListener('click', function(){
      all.disabled = true;
      cards.filter(function(c){ return !c.needsInput; }).reduce(function(pr, c){ return pr.then(function(){ return c.run(); }); }, Promise.resolve()).then(function(){ all.disabled = false; });
    });
  }
  function route(){ render((location.hash || '').replace('#', '')); }
  fetch('/api/tasks').then(function(r){ return r.json(); }).then(function(d){
    D = d;
    D.forEach(function(p){
      var b = el('button', 'tab'); b.type = 'button'; b.setAttribute('role', 'tab'); b.dataset.dir = p.dir;
      b.appendChild(document.createTextNode(nice(p.dir))); b.appendChild(el('span', null, String(p.items.length)));
      b.addEventListener('click', function(){ location.hash = p.dir; }); tabs.appendChild(b);
    });
    addEventListener('hashchange', route); route();
  });
})();
</script></body></html>
'''


def is_function_file(path):
    try:
        tree = ast.parse(open(path, encoding="utf-8").read())
    except (OSError, SyntaxError, UnicodeDecodeError):
        return False
    has_def = False
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            has_def = True
        elif isinstance(node, (ast.Import, ast.ImportFrom)):
            continue
        elif isinstance(node, ast.Expr) and isinstance(getattr(node, "value", None), ast.Constant):
            continue
        else:
            return False
    return has_def


def default_test(project, name):
    key = project + "/" + name
    if key in TESTS:
        return TESTS[key]
    mod = name[:-3]
    fn = re.sub(r"^\d+-", "", mod)
    return "%s = __import__('%s').%s\n# call it here, for example:\n# print(%s())\n" % (fn, mod, fn, fn)


def discover():
    projects = []
    for d in sorted(os.listdir(ROOT), key=lambda s: s.lower()):
        p = os.path.join(ROOT, d)
        if not (re.match(r"^python-[\w]+$", d) and os.path.isdir(p)):
            continue
        items = []
        names = [n for n in os.listdir(p) if re.match(r"^\d+-[\w]+(\.py)?$", n) and os.path.isfile(os.path.join(p, n))]
        names.sort(key=lambda n: int(n.split("-")[0]))
        for n in names:
            src = open(os.path.join(p, n), encoding="utf-8", errors="replace").read()
            if n.endswith(".py"):
                kind = "function" if is_function_file(os.path.join(p, n)) else "script"
            else:
                kind = "shell"
            items.append({"file": n, "kind": kind, "source": src,
                          "test": default_test(d, n) if kind == "function" else ""})
        projects.append({"dir": d, "items": items})
    return projects


def run_task(body):
    project, name = body.get("dir", ""), body.get("file", "")
    known = {(p["dir"], i["file"]): i for p in discover() for i in p["items"]}
    item = known.get((project, name))
    if item is None:
        return {"error": "Unknown task file."}
    cwd = os.path.join(ROOT, project)
    env = dict(os.environ)
    env["PYTHONIOENCODING"] = "utf-8"
    args = [a for a in body.get("args", "").split() if a]
    if item["kind"] == "function":
        cmd = [sys.executable, "-c", body.get("code", "")]
    elif item["kind"] == "script":
        cmd = [sys.executable, name] + args
    else:
        bash = shutil.which("bash")
        if not bash:
            return {"error": "This is a Bash script. Install Git Bash or WSL to run it from here."}
        cmd = [bash, name]
        for k in ("PYFILE", "PYCODE"):
            if body.get(k):
                env[k] = body[k]
    try:
        p = subprocess.run(cmd, cwd=cwd, env=env, capture_output=True, text=True,
                           encoding="utf-8", errors="replace", timeout=15, input="")
    except subprocess.TimeoutExpired:
        return {"error": "Stopped after 15 seconds."}
    return {"stdout": p.stdout, "stderr": p.stderr, "code": p.returncode}


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *a):
        pass

    def send(self, status, data, ctype="application/json; charset=utf-8"):
        raw = data if isinstance(data, bytes) else data.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(raw)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(raw)

    def do_GET(self):
        if self.path in ("/", "/index.html"):
            self.send(200, HTML.replace("__TOKEN__", TOKEN), "text/html; charset=utf-8")
        elif self.path == "/api/tasks":
            self.send(200, json.dumps(discover()))
        else:
            self.send(404, "{}")

    def do_POST(self):
        if self.path != "/api/run" or self.headers.get("X-Token") != TOKEN:
            self.send(403, json.dumps({"error": "Forbidden."}))
            return
        n = int(self.headers.get("Content-Length", "0") or 0)
        try:
            body = json.loads(self.rfile.read(n).decode("utf-8"))
        except ValueError:
            self.send(400, json.dumps({"error": "Bad request."}))
            return
        self.send(200, json.dumps(run_task(body)))


def main():
    server = None
    for port in range(8765, 8785):
        try:
            server = ThreadingHTTPServer(("127.0.0.1", port), Handler)
            break
        except OSError:
            continue
    if server is None:
        print("Could not find a free port between 8765 and 8784.")
        return 1
    url = "http://127.0.0.1:%d" % server.server_address[1]
    print("Task viewer running at " + url)
    print("Press Ctrl+C to stop.")
    threading.Timer(0.6, lambda: webbrowser.open(url)).start()
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopped.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
