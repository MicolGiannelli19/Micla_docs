---
title: Documentation
---

<div>
    <main class="pdoc">
            <section class="module-info">
                    <h1 class="modulename">
Documentation    </h1>

                
                        <input id="mod-client-view-source" class="view-source-toggle-state" type="checkbox" aria-hidden="true" tabindex="-1">

                        <label class="view-source-button" for="mod-client-view-source"><span>View Source</span></label>

                        <div class="pdoc-code codehilite"><pre><span></span><span id="L-1"><a href="#L-1"><span class="linenos">   1</span></a><span class="c1"># Standard imports</span>
</span><span id="L-2"><a href="#L-2"><span class="linenos">   2</span></a><span class="kn">import</span> <span class="nn">io</span>
</span><span id="L-3"><a href="#L-3"><span class="linenos">   3</span></a><span class="kn">import</span> <span class="nn">json</span>
</span><span id="L-4"><a href="#L-4"><span class="linenos">   4</span></a><span class="kn">from</span> <span class="nn">typing</span> <span class="kn">import</span> <span class="n">Union</span><span class="p">,</span> <span class="n">Optional</span><span class="p">,</span> <span class="n">Tuple</span>
</span><span id="L-5"><a href="#L-5"><span class="linenos">   5</span></a><span class="kn">from</span> <span class="nn">pprint</span> <span class="kn">import</span> <span class="n">pprint</span>
</span><span id="L-6"><a href="#L-6"><span class="linenos">   6</span></a><span class="kn">import</span> <span class="nn">time</span>
</span><span id="L-7"><a href="#L-7"><span class="linenos">   7</span></a>
</span><span id="L-8"><a href="#L-8"><span class="linenos">   8</span></a><span class="c1"># Third-party imports</span>
</span><span id="L-9"><a href="#L-9"><span class="linenos">   9</span></a><span class="kn">import</span> <span class="nn">pandas</span> <span class="k">as</span> <span class="nn">pd</span>
</span><span id="L-10"><a href="#L-10"><span class="linenos">  10</span></a><span class="kn">from</span> <span class="nn">typeguard</span> <span class="kn">import</span> <span class="n">typechecked</span>
</span><span id="L-11"><a href="#L-11"><span class="linenos">  11</span></a>
</span><span id="L-12"><a href="#L-12"><span class="linenos">  12</span></a><span class="c1"># Project imports</span>
</span><span id="L-13"><a href="#L-13"><span class="linenos">  13</span></a>
</span><span id="L-14"><a href="#L-14"><span class="linenos">  14</span></a>
</span><span id="L-15"><a href="#L-15"><span class="linenos">  15</span></a>
</span><span id="L-16"><a href="#L-16"><span class="linenos">  16</span></a><span class="c1">### Utility functions ###</span>
</span><span id="L-17"><a href="#L-17"><span class="linenos">  17</span></a>
</span><span id="L-18"><a href="#L-18"><span class="linenos">  18</span></a><span class="c1"># TODO: Move to utils.py?</span>
</span><span id="L-19"><a href="#L-19"><span class="linenos">  19</span></a>
</span><span id="L-20"><a href="#L-20"><span class="linenos">  20</span></a>
</span><span id="L-21"><a href="#L-21"><span class="linenos">  21</span></a><span class="k">def</span> <span class="nf">get_value_from_body</span><span class="p">(</span><span class="n">key</span><span class="p">:</span> <span class="nb">str</span><span class="p">,</span> <span class="n">body</span><span class="p">:</span> <span class="nb">dict</span><span class="p">):</span>
</span><span id="L-22"><a href="#L-22"><span class="linenos">  22</span></a>    <span class="c1"># Improve the error messaging and relate response from api.py directly here</span>
</span><span id="L-23"><a href="#L-23"><span class="linenos">  23</span></a>    <span class="k">if</span> <span class="n">key</span> <span class="ow">in</span> <span class="n">body</span><span class="o">.</span><span class="n">keys</span><span class="p">():</span>
</span><span id="L-24"><a href="#L-24"><span class="linenos">  24</span></a>        <span class="k">return</span> <span class="n">body</span><span class="p">[</span><span class="sa">f</span><span class="s2">&quot;</span><span class="si">{</span><span class="n">key</span><span class="si">}</span><span class="s2">&quot;</span><span class="p">]</span>
</span><span id="L-25"><a href="#L-25"><span class="linenos">  25</span></a>    <span class="k">else</span><span class="p">:</span>
</span><span id="L-26"><a href="#L-26"><span class="linenos">  26</span></a>        <span class="nb">print</span><span class="p">(</span><span class="n">body</span><span class="p">)</span>
</span><span id="L-27"><a href="#L-27"><span class="linenos">  27</span></a>        <span class="k">raise</span> <span class="ne">KeyError</span><span class="p">(</span><span class="sa">f</span><span class="s2">&quot;</span><span class="si">{</span><span class="n">key</span><span class="si">}</span><span class="s2"> not in API response body&quot;</span><span class="p">)</span>
</span><span id="L-28"><a href="#L-28"><span class="linenos">  28</span></a>
</span><span id="L-29"><a href="#L-29"><span class="linenos">  29</span></a>
</span><span id="L-30"><a href="#L-30"><span class="linenos">  30</span></a><span class="k">def</span> <span class="nf">_status_campaign</span><span class="p">(</span>
</span><span id="L-31"><a href="#L-31"><span class="linenos">  31</span></a>    <span class="n">campaign_id</span><span class="p">:</span> <span class="nb">str</span><span class="p">,</span> <span class="n">verbose</span><span class="p">:</span> <span class="n">Optional</span><span class="p">[</span><span class="nb">bool</span><span class="p">]</span> <span class="o">=</span> <span class="kc">False</span><span class="p">,</span> <span class="n">debug</span><span class="p">:</span> <span class="n">Optional</span><span class="p">[</span><span class="nb">bool</span><span class="p">]</span> <span class="o">=</span> <span class="kc">False</span>
</span><span id="L-32"><a href="#L-32"><span class="linenos">  32</span></a><span class="p">)</span> <span class="o">-&gt;</span> <span class="nb">dict</span><span class="p">:</span>
</span><span id="L-33"><a href="#L-33"><span class="linenos">  33</span></a>    <span class="n">response</span> <span class="o">=</span> <span class="n">api</span><span class="o">.</span><span class="n">get_status_model</span><span class="p">(</span><span class="n">campaign_id</span><span class="p">,</span> <span class="n">verbose</span><span class="o">=</span><span class="n">debug</span><span class="p">)</span>
</span><span id="L-34"><a href="#L-34"><span class="linenos">  34</span></a>    <span class="k">if</span> <span class="n">verbose</span><span class="p">:</span>
</span><span id="L-35"><a href="#L-35"><span class="linenos">  35</span></a>        <span class="n">message</span> <span class="o">=</span> <span class="n">_get_message</span><span class="p">(</span><span class="n">response</span><span class="p">)</span>
</span><span id="L-36"><a href="#L-36"><span class="linenos">  36</span></a>        <span class="nb">print</span><span class="p">(</span><span class="n">message</span><span class="p">)</span>
</span><span id="L-37"><a href="#L-37"><span class="linenos">  37</span></a>    <span class="k">return</span> <span class="n">response</span>
</span><span id="L-38"><a href="#L-38"><span class="linenos">  38</span></a>
</span><span id="L-39"><a href="#L-39"><span class="linenos">  39</span></a>
</span><span id="L-40"><a href="#L-40"><span class="linenos">  40</span></a><span class="k">def</span> <span class="nf">_get_csv_string</span><span class="p">(</span><span class="n">filepath_or_df</span><span class="p">:</span> <span class="n">Union</span><span class="p">[</span><span class="nb">str</span><span class="p">,</span> <span class="n">pd</span><span class="o">.</span><span class="n">DataFrame</span><span class="p">])</span> <span class="o">-&gt;</span> <span class="nb">str</span><span class="p">:</span>
</span><span id="L-41"><a href="#L-41"><span class="linenos">  41</span></a>    <span class="k">if</span> <span class="nb">type</span><span class="p">(</span><span class="n">filepath_or_df</span><span class="p">)</span> <span class="ow">is</span> <span class="nb">str</span><span class="p">:</span>
</span><span id="L-42"><a href="#L-42"><span class="linenos">  42</span></a>        <span class="n">filepath</span> <span class="o">=</span> <span class="n">filepath_or_df</span>
</span><span id="L-43"><a href="#L-43"><span class="linenos">  43</span></a>        <span class="n">csv_string</span> <span class="o">=</span> <span class="nb">open</span><span class="p">(</span><span class="n">filepath</span><span class="p">,</span> <span class="s2">&quot;r&quot;</span><span class="p">)</span><span class="o">.</span><span class="n">read</span><span class="p">()</span>
</span><span id="L-44"><a href="#L-44"><span class="linenos">  44</span></a>    <span class="k">elif</span> <span class="nb">type</span><span class="p">(</span><span class="n">filepath_or_df</span><span class="p">)</span> <span class="ow">is</span> <span class="n">pd</span><span class="o">.</span><span class="n">DataFrame</span><span class="p">:</span>
</span><span id="L-45"><a href="#L-45"><span class="linenos">  45</span></a>        <span class="n">df</span> <span class="o">=</span> <span class="n">filepath_or_df</span>
</span><span id="L-46"><a href="#L-46"><span class="linenos">  46</span></a>        <span class="n">buffer</span> <span class="o">=</span> <span class="n">io</span><span class="o">.</span><span class="n">StringIO</span><span class="p">()</span>
</span><span id="L-47"><a href="#L-47"><span class="linenos">  47</span></a>        <span class="n">df</span><span class="o">.</span><span class="n">to_csv</span><span class="p">(</span><span class="n">buffer</span><span class="p">,</span> <span class="n">index</span><span class="o">=</span><span class="kc">False</span><span class="p">)</span>
</span><span id="L-48"><a href="#L-48"><span class="linenos">  48</span></a>        <span class="n">csv_string</span> <span class="o">=</span> <span class="n">buffer</span><span class="o">.</span><span class="n">getvalue</span><span class="p">()</span>
</span><span id="L-49"><a href="#L-49"><span class="linenos">  49</span></a>    <span class="k">else</span><span class="p">:</span>
</span><span id="L-50"><a href="#L-50"><span class="linenos">  50</span></a>        <span class="k">raise</span> <span class="ne">ValueError</span><span class="p">(</span><span class="s2">&quot;filepath_or_df must be a string or pandas dataframe&quot;</span><span class="p">)</span>
</span><span id="L-51"><a href="#L-51"><span class="linenos">  51</span></a>    <span class="k">return</span> <span class="n">csv_string</span>
</span><span id="L-52"><a href="#L-52"><span class="linenos">  52</span></a>
</span><span id="L-53"><a href="#L-53"><span class="linenos">  53</span></a>
</span><span id="L-54"><a href="#L-54"><span class="linenos">  54</span></a><span class="k">def</span> <span class="nf">_use_campaign</span><span class="p">(</span>
</span><span id="L-55"><a href="#L-55"><span class="linenos">  55</span></a>    <span class="n">campaign_id</span><span class="p">:</span> <span class="nb">str</span><span class="p">,</span>
</span><span id="L-56"><a href="#L-56"><span class="linenos">  56</span></a>    <span class="n">method</span><span class="p">:</span> <span class="nb">str</span><span class="p">,</span>
</span><span id="L-57"><a href="#L-57"><span class="linenos">  57</span></a>    <span class="n">filepath_or_df</span><span class="p">:</span> <span class="n">Optional</span><span class="p">[</span><span class="n">Union</span><span class="p">[</span><span class="nb">str</span><span class="p">,</span> <span class="n">pd</span><span class="o">.</span><span class="n">DataFrame</span><span class="p">]]</span> <span class="o">=</span> <span class="kc">None</span><span class="p">,</span>
</span><span id="L-58"><a href="#L-58"><span class="linenos">  58</span></a>    <span class="n">filepath_or_df_std</span><span class="p">:</span> <span class="n">Optional</span><span class="p">[</span><span class="n">Union</span><span class="p">[</span><span class="nb">str</span><span class="p">,</span> <span class="n">pd</span><span class="o">.</span><span class="n">DataFrame</span><span class="p">]]</span> <span class="o">=</span> <span class="kc">None</span><span class="p">,</span>
</span><span id="L-59"><a href="#L-59"><span class="linenos">  59</span></a>    <span class="n">processor</span><span class="p">:</span> <span class="n">Optional</span><span class="p">[</span><span class="nb">str</span><span class="p">]</span> <span class="o">=</span> <span class="s2">&quot;cpu&quot;</span><span class="p">,</span>
</span><span id="L-60"><a href="#L-60"><span class="linenos">  60</span></a>    <span class="n">verbose</span><span class="p">:</span> <span class="n">Optional</span><span class="p">[</span><span class="nb">bool</span><span class="p">]</span> <span class="o">=</span> <span class="kc">False</span><span class="p">,</span>
</span><span id="L-61"><a href="#L-61"><span class="linenos">  61</span></a>    <span class="n">debug</span><span class="p">:</span> <span class="n">Optional</span><span class="p">[</span><span class="nb">bool</span><span class="p">]</span> <span class="o">=</span> <span class="kc">False</span><span class="p">,</span>
</span><span id="L-62"><a href="#L-62"><span class="linenos">  62</span></a>    <span class="o">**</span><span class="n">kwargs</span><span class="p">,</span>
</span><span id="L-63"><a href="#L-63"><span class="linenos">  63</span></a><span class="p">)</span> <span class="o">-&gt;</span> <span class="n">io</span><span class="o">.</span><span class="n">StringIO</span><span class="p">:</span>
</span><span id="L-64"><a href="#L-64"><span class="linenos">  64</span></a>    <span class="k">if</span> <span class="n">filepath_or_df</span> <span class="ow">is</span> <span class="ow">not</span> <span class="kc">None</span><span class="p">:</span>
</span><span id="L-65"><a href="#L-65"><span class="linenos">  65</span></a>        <span class="n">data_csv</span> <span class="o">=</span> <span class="n">_get_csv_string</span><span class="p">(</span><span class="n">filepath_or_df</span><span class="p">)</span>
</span><span id="L-66"><a href="#L-66"><span class="linenos">  66</span></a>    <span class="k">else</span><span class="p">:</span>
</span><span id="L-67"><a href="#L-67"><span class="linenos">  67</span></a>        <span class="n">data_csv</span> <span class="o">=</span> <span class="kc">None</span>
</span><span id="L-68"><a href="#L-68"><span class="linenos">  68</span></a>    <span class="k">if</span> <span class="n">filepath_or_df_std</span> <span class="ow">is</span> <span class="ow">not</span> <span class="kc">None</span><span class="p">:</span>
</span><span id="L-69"><a href="#L-69"><span class="linenos">  69</span></a>        <span class="n">data_std_csv</span> <span class="o">=</span> <span class="n">_get_csv_string</span><span class="p">(</span><span class="n">filepath_or_df_std</span><span class="p">)</span>
</span><span id="L-70"><a href="#L-70"><span class="linenos">  70</span></a>    <span class="k">else</span><span class="p">:</span>
</span><span id="L-71"><a href="#L-71"><span class="linenos">  71</span></a>        <span class="n">data_std_csv</span> <span class="o">=</span> <span class="kc">None</span>
</span><span id="L-72"><a href="#L-72"><span class="linenos">  72</span></a>    <span class="n">response</span> <span class="o">=</span> <span class="n">api</span><span class="o">.</span><span class="n">use_model</span><span class="p">(</span>
</span><span id="L-73"><a href="#L-73"><span class="linenos">  73</span></a>        <span class="n">campaign_id</span><span class="p">,</span>
</span><span id="L-74"><a href="#L-74"><span class="linenos">  74</span></a>        <span class="n">method</span><span class="p">,</span>
</span><span id="L-75"><a href="#L-75"><span class="linenos">  75</span></a>        <span class="n">data_csv</span><span class="o">=</span><span class="n">data_csv</span><span class="p">,</span>
</span><span id="L-76"><a href="#L-76"><span class="linenos">  76</span></a>        <span class="n">data_std_csv</span><span class="o">=</span><span class="n">data_std_csv</span><span class="p">,</span>
</span><span id="L-77"><a href="#L-77"><span class="linenos">  77</span></a>        <span class="n">processor</span><span class="o">=</span><span class="n">processor</span><span class="p">,</span>
</span><span id="L-78"><a href="#L-78"><span class="linenos">  78</span></a>        <span class="n">verbose</span><span class="o">=</span><span class="n">debug</span><span class="p">,</span>
</span><span id="L-79"><a href="#L-79"><span class="linenos">  79</span></a>        <span class="o">**</span><span class="n">kwargs</span><span class="p">,</span>
</span><span id="L-80"><a href="#L-80"><span class="linenos">  80</span></a>    <span class="p">)</span>
</span><span id="L-81"><a href="#L-81"><span class="linenos">  81</span></a>    <span class="n">output_csv</span> <span class="o">=</span> <span class="n">get_value_from_body</span><span class="p">(</span><span class="s2">&quot;dataframe&quot;</span><span class="p">,</span> <span class="n">response</span><span class="p">)</span>
</span><span id="L-82"><a href="#L-82"><span class="linenos">  82</span></a>
</span><span id="L-83"><a href="#L-83"><span class="linenos">  83</span></a>    <span class="k">return</span> <span class="n">io</span><span class="o">.</span><span class="n">StringIO</span><span class="p">(</span><span class="n">output_csv</span><span class="p">)</span>
</span><span id="L-84"><a href="#L-84"><span class="linenos">  84</span></a>
</span><span id="L-85"><a href="#L-85"><span class="linenos">  85</span></a>
</span><span id="L-86"><a href="#L-86"><span class="linenos">  86</span></a><span class="k">def</span> <span class="nf">_get_message</span><span class="p">(</span><span class="n">response</span><span class="p">:</span> <span class="nb">dict</span><span class="p">)</span> <span class="o">-&gt;</span> <span class="nb">str</span><span class="p">:</span>
</span><span id="L-87"><a href="#L-87"><span class="linenos">  87</span></a>    <span class="c1"># TODO: This could be a method of the response object</span>
</span><span id="L-88"><a href="#L-88"><span class="linenos">  88</span></a>    <span class="c1"># TODO: This should be better</span>
</span><span id="L-89"><a href="#L-89"><span class="linenos">  89</span></a>    <span class="k">try</span><span class="p">:</span>
</span><span id="L-90"><a href="#L-90"><span class="linenos">  90</span></a>        <span class="n">message</span> <span class="o">=</span> <span class="n">response</span><span class="p">[</span><span class="s2">&quot;message&quot;</span><span class="p">]</span>
</span><span id="L-91"><a href="#L-91"><span class="linenos">  91</span></a>    <span class="k">except</span><span class="p">:</span>
</span><span id="L-92"><a href="#L-92"><span class="linenos">  92</span></a>        <span class="n">message</span> <span class="o">=</span> <span class="n">response</span>
</span><span id="L-93"><a href="#L-93"><span class="linenos">  93</span></a>    <span class="k">return</span> <span class="n">message</span>
</span><span id="L-94"><a href="#L-94"><span class="linenos">  94</span></a>
</span><span id="L-95"><a href="#L-95"><span class="linenos">  95</span></a>
</span><span id="L-96"><a href="#L-96"><span class="linenos">  96</span></a><span class="c1">### ###</span>
</span><span id="L-97"><a href="#L-97"><span class="linenos">  97</span></a>
</span><span id="L-98"><a href="#L-98"><span class="linenos">  98</span></a><span class="c1">### General functions ###</span>
</span><span id="L-99"><a href="#L-99"><span class="linenos">  99</span></a>
</span><span id="L-100"><a href="#L-100"><span class="linenos"> 100</span></a>
</span><span id="L-101"><a href="#L-101"><span class="linenos"> 101</span></a><span class="nd">@typechecked</span>
</span><span id="L-102"><a href="#L-102"><span class="linenos"> 102</span></a><span class="k">def</span> <span class="nf">get_user_information</span><span class="p">(</span>
</span><span id="L-103"><a href="#L-103"><span class="linenos"> 103</span></a>    <span class="n">verbose</span><span class="p">:</span> <span class="n">Optional</span><span class="p">[</span><span class="nb">bool</span><span class="p">]</span> <span class="o">=</span> <span class="kc">False</span><span class="p">,</span> <span class="n">debug</span><span class="p">:</span> <span class="n">Optional</span><span class="p">[</span><span class="nb">bool</span><span class="p">]</span> <span class="o">=</span> <span class="kc">False</span>
</span><span id="L-104"><a href="#L-104"><span class="linenos"> 104</span></a><span class="p">)</span> <span class="o">-&gt;</span> <span class="nb">dict</span><span class="p">:</span>
</span><span id="L-105"><a href="#L-105"><span class="linenos"> 105</span></a><span class="w">    </span><span class="sd">&quot;&quot;&quot;</span>
</span><span id="L-106"><a href="#L-106"><span class="linenos"> 106</span></a><span class="sd">    # Get user information</span>
</span><span id="L-107"><a href="#L-107"><span class="linenos"> 107</span></a>
</span><span id="L-108"><a href="#L-108"><span class="linenos"> 108</span></a><span class="sd">    Get information about the user</span>
</span><span id="L-109"><a href="#L-109"><span class="linenos"> 109</span></a>
</span><span id="L-110"><a href="#L-110"><span class="linenos"> 110</span></a><span class="sd">    ## Arguments</span>
</span><span id="L-111"><a href="#L-111"><span class="linenos"> 111</span></a>
</span><span id="L-112"><a href="#L-112"><span class="linenos"> 112</span></a><span class="sd">    - `verbose`: `bool`, Optional, determining level of information returned to the user</span>
</span><span id="L-113"><a href="#L-113"><span class="linenos"> 113</span></a><span class="sd">    - `debug`: `bool`, Optional, determining level of information logged on the server</span>
</span><span id="L-114"><a href="#L-114"><span class="linenos"> 114</span></a>
</span><span id="L-115"><a href="#L-115"><span class="linenos"> 115</span></a><span class="sd">    ## Returns</span>
</span><span id="L-116"><a href="#L-116"><span class="linenos"> 116</span></a>
</span><span id="L-117"><a href="#L-117"><span class="linenos"> 117</span></a><span class="sd">    - `dict` containing user information</span>
</span><span id="L-118"><a href="#L-118"><span class="linenos"> 118</span></a>
</span><span id="L-119"><a href="#L-119"><span class="linenos"> 119</span></a><span class="sd">    ## Example</span>
</span><span id="L-120"><a href="#L-120"><span class="linenos"> 120</span></a><span class="sd">    ```python</span>
</span><span id="L-121"><a href="#L-121"><span class="linenos"> 121</span></a><span class="sd">    import twinlab as tl</span>
</span><span id="L-122"><a href="#L-122"><span class="linenos"> 122</span></a>
</span><span id="L-123"><a href="#L-123"><span class="linenos"> 123</span></a><span class="sd">    user_info = tl.get_user_information()</span>
</span><span id="L-124"><a href="#L-124"><span class="linenos"> 124</span></a><span class="sd">    print(user_info)</span>
</span><span id="L-125"><a href="#L-125"><span class="linenos"> 125</span></a><span class="sd">    ```</span>
</span><span id="L-126"><a href="#L-126"><span class="linenos"> 126</span></a><span class="sd">    &quot;&quot;&quot;</span>
</span><span id="L-127"><a href="#L-127"><span class="linenos"> 127</span></a>    <span class="n">response</span> <span class="o">=</span> <span class="n">api</span><span class="o">.</span><span class="n">get_user</span><span class="p">(</span><span class="n">verbose</span><span class="o">=</span><span class="n">debug</span><span class="p">)</span>
</span><span id="L-128"><a href="#L-128"><span class="linenos"> 128</span></a>    <span class="n">user_info</span> <span class="o">=</span> <span class="n">response</span>
</span><span id="L-129"><a href="#L-129"><span class="linenos"> 129</span></a>    <span class="k">if</span> <span class="n">verbose</span><span class="p">:</span>
</span><span id="L-130"><a href="#L-130"><span class="linenos"> 130</span></a>        <span class="nb">print</span><span class="p">(</span><span class="s2">&quot;User information:&quot;</span><span class="p">)</span>
</span><span id="L-131"><a href="#L-131"><span class="linenos"> 131</span></a>        <span class="n">pprint</span><span class="p">(</span><span class="n">user_info</span><span class="p">,</span> <span class="n">compact</span><span class="o">=</span><span class="kc">True</span><span class="p">,</span> <span class="n">sort_dicts</span><span class="o">=</span><span class="kc">False</span><span class="p">)</span>
</span><span id="L-132"><a href="#L-132"><span class="linenos"> 132</span></a>    <span class="k">return</span> <span class="n">user_info</span>
</span><span id="L-133"><a href="#L-133"><span class="linenos"> 133</span></a>
</span><span id="L-134"><a href="#L-134"><span class="linenos"> 134</span></a>
</span><span id="L-135"><a href="#L-135"><span class="linenos"> 135</span></a><span class="nd">@typechecked</span>
</span><span id="L-136"><a href="#L-136"><span class="linenos"> 136</span></a><span class="k">def</span> <span class="nf">get_versions</span><span class="p">(</span>
</span><span id="L-137"><a href="#L-137"><span class="linenos"> 137</span></a>    <span class="n">verbose</span><span class="p">:</span> <span class="n">Optional</span><span class="p">[</span><span class="nb">bool</span><span class="p">]</span> <span class="o">=</span> <span class="kc">False</span><span class="p">,</span> <span class="n">debug</span><span class="p">:</span> <span class="n">Optional</span><span class="p">[</span><span class="nb">bool</span><span class="p">]</span> <span class="o">=</span> <span class="kc">False</span>
</span><span id="L-138"><a href="#L-138"><span class="linenos"> 138</span></a><span class="p">)</span> <span class="o">-&gt;</span> <span class="nb">dict</span><span class="p">:</span>
</span><span id="L-139"><a href="#L-139"><span class="linenos"> 139</span></a><span class="w">    </span><span class="sd">&quot;&quot;&quot;</span>
</span><span id="L-140"><a href="#L-140"><span class="linenos"> 140</span></a><span class="sd">    # Get versions</span>
</span><span id="L-141"><a href="#L-141"><span class="linenos"> 141</span></a>
</span><span id="L-142"><a href="#L-142"><span class="linenos"> 142</span></a><span class="sd">    Get information about the twinLab version being used</span>
</span><span id="L-143"><a href="#L-143"><span class="linenos"> 143</span></a>
</span><span id="L-144"><a href="#L-144"><span class="linenos"> 144</span></a><span class="sd">    ## Arguments</span>
</span><span id="L-145"><a href="#L-145"><span class="linenos"> 145</span></a>
</span><span id="L-146"><a href="#L-146"><span class="linenos"> 146</span></a><span class="sd">    - `verbose`: `bool`, Optional, determining level of information returned to the user</span>
</span><span id="L-147"><a href="#L-147"><span class="linenos"> 147</span></a><span class="sd">    - `debug`: `bool`, Optional, determining level of information logged on the server</span>
</span><span id="L-148"><a href="#L-148"><span class="linenos"> 148</span></a>
</span><span id="L-149"><a href="#L-149"><span class="linenos"> 149</span></a><span class="sd">    ## Returns</span>
</span><span id="L-150"><a href="#L-150"><span class="linenos"> 150</span></a>
</span><span id="L-151"><a href="#L-151"><span class="linenos"> 151</span></a><span class="sd">    - `dict` containing version information</span>
</span><span id="L-152"><a href="#L-152"><span class="linenos"> 152</span></a>
</span><span id="L-153"><a href="#L-153"><span class="linenos"> 153</span></a><span class="sd">    ## Example</span>
</span><span id="L-154"><a href="#L-154"><span class="linenos"> 154</span></a><span class="sd">    ```python</span>
</span><span id="L-155"><a href="#L-155"><span class="linenos"> 155</span></a><span class="sd">    import twinlab as tl</span>
</span><span id="L-156"><a href="#L-156"><span class="linenos"> 156</span></a>
</span><span id="L-157"><a href="#L-157"><span class="linenos"> 157</span></a><span class="sd">    version_info = tl.get_versions()</span>
</span><span id="L-158"><a href="#L-158"><span class="linenos"> 158</span></a><span class="sd">    print(version_info)</span>
</span><span id="L-159"><a href="#L-159"><span class="linenos"> 159</span></a><span class="sd">    ```</span>
</span><span id="L-160"><a href="#L-160"><span class="linenos"> 160</span></a><span class="sd">    &quot;&quot;&quot;</span>
</span><span id="L-161"><a href="#L-161"><span class="linenos"> 161</span></a>    <span class="n">response</span> <span class="o">=</span> <span class="n">api</span><span class="o">.</span><span class="n">get_versions</span><span class="p">(</span><span class="n">verbose</span><span class="o">=</span><span class="n">debug</span><span class="p">)</span>
</span><span id="L-162"><a href="#L-162"><span class="linenos"> 162</span></a>    <span class="n">version_info</span> <span class="o">=</span> <span class="n">response</span>
</span><span id="L-163"><a href="#L-163"><span class="linenos"> 163</span></a>    <span class="k">if</span> <span class="n">verbose</span><span class="p">:</span>
</span><span id="L-164"><a href="#L-164"><span class="linenos"> 164</span></a>        <span class="nb">print</span><span class="p">(</span><span class="s2">&quot;Version information:&quot;</span><span class="p">)</span>
</span><span id="L-165"><a href="#L-165"><span class="linenos"> 165</span></a>        <span class="n">pprint</span><span class="p">(</span><span class="n">version_info</span><span class="p">,</span> <span class="n">compact</span><span class="o">=</span><span class="kc">True</span><span class="p">,</span> <span class="n">sort_dicts</span><span class="o">=</span><span class="kc">False</span><span class="p">)</span>
</span><span id="L-166"><a href="#L-166"><span class="linenos"> 166</span></a>    <span class="k">return</span> <span class="n">version_info</span>
</span><span id="L-167"><a href="#L-167"><span class="linenos"> 167</span></a>
</span><span id="L-168"><a href="#L-168"><span class="linenos"> 168</span></a>
</span><span id="L-169"><a href="#L-169"><span class="linenos"> 169</span></a><span class="c1">### ###</span>
</span><span id="L-170"><a href="#L-170"><span class="linenos"> 170</span></a>
</span><span id="L-171"><a href="#L-171"><span class="linenos"> 171</span></a><span class="c1">### Dataset functions ###</span>
</span><span id="L-172"><a href="#L-172"><span class="linenos"> 172</span></a>
</span><span id="L-173"><a href="#L-173"><span class="linenos"> 173</span></a>
</span><span id="L-174"><a href="#L-174"><span class="linenos"> 174</span></a><span class="nd">@typechecked</span>
</span><span id="L-175"><a href="#L-175"><span class="linenos"> 175</span></a><span class="k">def</span> <span class="nf">upload_dataset</span><span class="p">(</span>
</span><span id="L-176"><a href="#L-176"><span class="linenos"> 176</span></a>    <span class="n">filepath_or_df</span><span class="p">:</span> <span class="n">Union</span><span class="p">[</span><span class="nb">str</span><span class="p">,</span> <span class="n">pd</span><span class="o">.</span><span class="n">DataFrame</span><span class="p">],</span>
</span><span id="L-177"><a href="#L-177"><span class="linenos"> 177</span></a>    <span class="n">dataset_id</span><span class="p">:</span> <span class="nb">str</span><span class="p">,</span>
</span><span id="L-178"><a href="#L-178"><span class="linenos"> 178</span></a>    <span class="n">use_upload_url</span><span class="p">:</span> <span class="n">Optional</span><span class="p">[</span><span class="nb">bool</span><span class="p">]</span> <span class="o">=</span> <span class="kc">True</span><span class="p">,</span>
</span><span id="L-179"><a href="#L-179"><span class="linenos"> 179</span></a>    <span class="n">verbose</span><span class="p">:</span> <span class="n">Optional</span><span class="p">[</span><span class="nb">bool</span><span class="p">]</span> <span class="o">=</span> <span class="kc">False</span><span class="p">,</span>
</span><span id="L-180"><a href="#L-180"><span class="linenos"> 180</span></a>    <span class="n">debug</span><span class="p">:</span> <span class="n">Optional</span><span class="p">[</span><span class="nb">bool</span><span class="p">]</span> <span class="o">=</span> <span class="kc">False</span><span class="p">,</span>
</span><span id="L-181"><a href="#L-181"><span class="linenos"> 181</span></a><span class="p">)</span> <span class="o">-&gt;</span> <span class="kc">None</span><span class="p">:</span>
</span><span id="L-182"><a href="#L-182"><span class="linenos"> 182</span></a><span class="w">    </span><span class="sd">&quot;&quot;&quot;</span>
</span><span id="L-183"><a href="#L-183"><span class="linenos"> 183</span></a><span class="sd">    # Upload dataset</span>
</span><span id="L-184"><a href="#L-184"><span class="linenos"> 184</span></a>
</span><span id="L-185"><a href="#L-185"><span class="linenos"> 185</span></a><span class="sd">    Upload a dataset to the `twinLab` cloud so that it can be queried and used for training.</span>
</span><span id="L-186"><a href="#L-186"><span class="linenos"> 186</span></a>
</span><span id="L-187"><a href="#L-187"><span class="linenos"> 187</span></a><span class="sd">    ## Arguments</span>
</span><span id="L-188"><a href="#L-188"><span class="linenos"> 188</span></a>
</span><span id="L-189"><a href="#L-189"><span class="linenos"> 189</span></a><span class="sd">    - `filepath_or_df`: `str` | `Dataframe`, location of csv dataset on local machine or `pandas` dataframe</span>
</span><span id="L-190"><a href="#L-190"><span class="linenos"> 190</span></a><span class="sd">    - `dataset_id`: `str`, name for the dataset when saved to the twinLab cloud</span>
</span><span id="L-191"><a href="#L-191"><span class="linenos"> 191</span></a><span class="sd">    **Warning:** If the `dataset_id` already exists for the current cloud account, it will be overwritten by the</span>
</span><span id="L-192"><a href="#L-192"><span class="linenos"> 192</span></a><span class="sd">    newly uploaded dataset</span>
</span><span id="L-193"><a href="#L-193"><span class="linenos"> 193</span></a><span class="sd">    - `use_upload_url`: `bool`, Optional, determining whether to upload via a pre-signed url or directly to the server</span>
</span><span id="L-194"><a href="#L-194"><span class="linenos"> 194</span></a><span class="sd">    - `verbose`: `bool`, Optional, determining level of information returned to the user</span>
</span><span id="L-195"><a href="#L-195"><span class="linenos"> 195</span></a><span class="sd">    - `debug`: `bool`, Optional,determining level of information logged on the server</span>
</span><span id="L-196"><a href="#L-196"><span class="linenos"> 196</span></a>
</span><span id="L-197"><a href="#L-197"><span class="linenos"> 197</span></a><span class="sd">    **NOTE:** Local data must be a CSV file, working data should be a pandas Dataframe.</span>
</span><span id="L-198"><a href="#L-198"><span class="linenos"> 198</span></a>
</span><span id="L-199"><a href="#L-199"><span class="linenos"> 199</span></a><span class="sd">    ## Examples</span>
</span><span id="L-200"><a href="#L-200"><span class="linenos"> 200</span></a>
</span><span id="L-201"><a href="#L-201"><span class="linenos"> 201</span></a><span class="sd">    Upload a local file:</span>
</span><span id="L-202"><a href="#L-202"><span class="linenos"> 202</span></a><span class="sd">    ```python</span>
</span><span id="L-203"><a href="#L-203"><span class="linenos"> 203</span></a><span class="sd">    import twinlab as tl</span>
</span><span id="L-204"><a href="#L-204"><span class="linenos"> 204</span></a>
</span><span id="L-205"><a href="#L-205"><span class="linenos"> 205</span></a><span class="sd">    data_filepath = &quot;path/to/dataset.csv&quot;</span>
</span><span id="L-206"><a href="#L-206"><span class="linenos"> 206</span></a><span class="sd">    tl.upload_dataset(data_filepath, &quot;my_dataset&quot;)</span>
</span><span id="L-207"><a href="#L-207"><span class="linenos"> 207</span></a><span class="sd">    ```</span>
</span><span id="L-208"><a href="#L-208"><span class="linenos"> 208</span></a>
</span><span id="L-209"><a href="#L-209"><span class="linenos"> 209</span></a><span class="sd">    Upload a `pandas` dataframe:</span>
</span><span id="L-210"><a href="#L-210"><span class="linenos"> 210</span></a><span class="sd">    ```python</span>
</span><span id="L-211"><a href="#L-211"><span class="linenos"> 211</span></a><span class="sd">    import pandas as pd</span>
</span><span id="L-212"><a href="#L-212"><span class="linenos"> 212</span></a><span class="sd">    import twinlab as tl</span>
</span><span id="L-213"><a href="#L-213"><span class="linenos"> 213</span></a>
</span><span id="L-214"><a href="#L-214"><span class="linenos"> 214</span></a><span class="sd">    df = pd.DataFrame({&#39;X&#39;: [1, 2, 3, 4], &#39;y&#39;: [1, 4, 9, 16]})</span>
</span><span id="L-215"><a href="#L-215"><span class="linenos"> 215</span></a><span class="sd">    tl.upload_dataset(df, &quot;my_dataset&quot;)</span>
</span><span id="L-216"><a href="#L-216"><span class="linenos"> 216</span></a><span class="sd">    ```</span>
</span><span id="L-217"><a href="#L-217"><span class="linenos"> 217</span></a><span class="sd">    &quot;&quot;&quot;</span>
</span><span id="L-218"><a href="#L-218"><span class="linenos"> 218</span></a>
</span><span id="L-219"><a href="#L-219"><span class="linenos"> 219</span></a>    <span class="c1"># Upload the file (either via link or directly)</span>
</span><span id="L-220"><a href="#L-220"><span class="linenos"> 220</span></a>    <span class="k">if</span> <span class="n">use_upload_url</span><span class="p">:</span>
</span><span id="L-221"><a href="#L-221"><span class="linenos"> 221</span></a>        <span class="n">response</span> <span class="o">=</span> <span class="n">api</span><span class="o">.</span><span class="n">generate_upload_url</span><span class="p">(</span><span class="n">dataset_id</span><span class="p">,</span> <span class="n">verbose</span><span class="o">=</span><span class="n">debug</span><span class="p">)</span>
</span><span id="L-222"><a href="#L-222"><span class="linenos"> 222</span></a>        <span class="n">upload_url</span> <span class="o">=</span> <span class="n">get_value_from_body</span><span class="p">(</span><span class="s2">&quot;url&quot;</span><span class="p">,</span> <span class="n">response</span><span class="p">)</span>
</span><span id="L-223"><a href="#L-223"><span class="linenos"> 223</span></a>        <span class="k">if</span> <span class="nb">type</span><span class="p">(</span><span class="n">filepath_or_df</span><span class="p">)</span> <span class="ow">is</span> <span class="nb">str</span><span class="p">:</span>
</span><span id="L-224"><a href="#L-224"><span class="linenos"> 224</span></a>            <span class="n">filepath</span> <span class="o">=</span> <span class="n">filepath_or_df</span>
</span><span id="L-225"><a href="#L-225"><span class="linenos"> 225</span></a>            <span class="n">utils</span><span class="o">.</span><span class="n">upload_file_to_presigned_url</span><span class="p">(</span>
</span><span id="L-226"><a href="#L-226"><span class="linenos"> 226</span></a>                <span class="n">filepath</span><span class="p">,</span> <span class="n">upload_url</span><span class="p">,</span> <span class="n">verbose</span><span class="o">=</span><span class="n">verbose</span><span class="p">,</span> <span class="n">check</span><span class="o">=</span><span class="n">settings</span><span class="o">.</span><span class="n">CHECK_DATASETS</span>
</span><span id="L-227"><a href="#L-227"><span class="linenos"> 227</span></a>            <span class="p">)</span>
</span><span id="L-228"><a href="#L-228"><span class="linenos"> 228</span></a>        <span class="k">elif</span> <span class="nb">type</span><span class="p">(</span><span class="n">filepath_or_df</span><span class="p">)</span> <span class="ow">is</span> <span class="n">pd</span><span class="o">.</span><span class="n">DataFrame</span><span class="p">:</span>
</span><span id="L-229"><a href="#L-229"><span class="linenos"> 229</span></a>            <span class="n">df</span> <span class="o">=</span> <span class="n">filepath_or_df</span>
</span><span id="L-230"><a href="#L-230"><span class="linenos"> 230</span></a>            <span class="n">utils</span><span class="o">.</span><span class="n">upload_dataframe_to_presigned_url</span><span class="p">(</span>
</span><span id="L-231"><a href="#L-231"><span class="linenos"> 231</span></a>                <span class="n">df</span><span class="p">,</span> <span class="n">upload_url</span><span class="p">,</span> <span class="n">verbose</span><span class="o">=</span><span class="n">verbose</span><span class="p">,</span> <span class="n">check</span><span class="o">=</span><span class="n">settings</span><span class="o">.</span><span class="n">CHECK_DATASETS</span>
</span><span id="L-232"><a href="#L-232"><span class="linenos"> 232</span></a>            <span class="p">)</span>
</span><span id="L-233"><a href="#L-233"><span class="linenos"> 233</span></a>        <span class="k">else</span><span class="p">:</span>
</span><span id="L-234"><a href="#L-234"><span class="linenos"> 234</span></a>            <span class="k">raise</span> <span class="ne">ValueError</span><span class="p">(</span><span class="s2">&quot;filepath_or_df must be a string or pandas dataframe&quot;</span><span class="p">)</span>
</span><span id="L-235"><a href="#L-235"><span class="linenos"> 235</span></a>        <span class="k">if</span> <span class="n">verbose</span><span class="p">:</span>
</span><span id="L-236"><a href="#L-236"><span class="linenos"> 236</span></a>            <span class="nb">print</span><span class="p">(</span><span class="s2">&quot;Processing dataset.&quot;</span><span class="p">)</span>
</span><span id="L-237"><a href="#L-237"><span class="linenos"> 237</span></a>        <span class="n">response</span> <span class="o">=</span> <span class="n">api</span><span class="o">.</span><span class="n">process_uploaded_dataset</span><span class="p">(</span><span class="n">dataset_id</span><span class="p">,</span> <span class="n">verbose</span><span class="o">=</span><span class="n">debug</span><span class="p">)</span>
</span><span id="L-238"><a href="#L-238"><span class="linenos"> 238</span></a>
</span><span id="L-239"><a href="#L-239"><span class="linenos"> 239</span></a>    <span class="k">else</span><span class="p">:</span>
</span><span id="L-240"><a href="#L-240"><span class="linenos"> 240</span></a>        <span class="n">csv_string</span> <span class="o">=</span> <span class="n">_get_csv_string</span><span class="p">(</span><span class="n">filepath_or_df</span><span class="p">)</span>
</span><span id="L-241"><a href="#L-241"><span class="linenos"> 241</span></a>        <span class="n">response</span> <span class="o">=</span> <span class="n">api</span><span class="o">.</span><span class="n">upload_dataset</span><span class="p">(</span><span class="n">dataset_id</span><span class="p">,</span> <span class="n">csv_string</span><span class="p">,</span> <span class="n">verbose</span><span class="o">=</span><span class="n">debug</span><span class="p">)</span>
</span><span id="L-242"><a href="#L-242"><span class="linenos"> 242</span></a>
</span><span id="L-243"><a href="#L-243"><span class="linenos"> 243</span></a>    <span class="k">if</span> <span class="n">verbose</span><span class="p">:</span>
</span><span id="L-244"><a href="#L-244"><span class="linenos"> 244</span></a>        <span class="n">message</span> <span class="o">=</span> <span class="n">_get_message</span><span class="p">(</span><span class="n">response</span><span class="p">)</span>
</span><span id="L-245"><a href="#L-245"><span class="linenos"> 245</span></a>        <span class="nb">print</span><span class="p">(</span><span class="n">message</span><span class="p">)</span>
</span><span id="L-246"><a href="#L-246"><span class="linenos"> 246</span></a>
</span><span id="L-247"><a href="#L-247"><span class="linenos"> 247</span></a>
</span><span id="L-248"><a href="#L-248"><span class="linenos"> 248</span></a><span class="nd">@typechecked</span>
</span><span id="L-249"><a href="#L-249"><span class="linenos"> 249</span></a><span class="k">def</span> <span class="nf">list_datasets</span><span class="p">(</span>
</span><span id="L-250"><a href="#L-250"><span class="linenos"> 250</span></a>    <span class="n">verbose</span><span class="p">:</span> <span class="n">Optional</span><span class="p">[</span><span class="nb">bool</span><span class="p">]</span> <span class="o">=</span> <span class="kc">False</span><span class="p">,</span> <span class="n">debug</span><span class="p">:</span> <span class="n">Optional</span><span class="p">[</span><span class="nb">bool</span><span class="p">]</span> <span class="o">=</span> <span class="kc">False</span>
</span><span id="L-251"><a href="#L-251"><span class="linenos"> 251</span></a><span class="p">)</span> <span class="o">-&gt;</span> <span class="nb">list</span><span class="p">:</span>
</span><span id="L-252"><a href="#L-252"><span class="linenos"> 252</span></a><span class="w">    </span><span class="sd">&quot;&quot;&quot;</span>
</span><span id="L-253"><a href="#L-253"><span class="linenos"> 253</span></a><span class="sd">    # List datasets</span>
</span><span id="L-254"><a href="#L-254"><span class="linenos"> 254</span></a>
</span><span id="L-255"><a href="#L-255"><span class="linenos"> 255</span></a><span class="sd">    List datasets that have been uploaded to the `twinLab` cloud</span>
</span><span id="L-256"><a href="#L-256"><span class="linenos"> 256</span></a>
</span><span id="L-257"><a href="#L-257"><span class="linenos"> 257</span></a><span class="sd">    ## Arguments</span>
</span><span id="L-258"><a href="#L-258"><span class="linenos"> 258</span></a>
</span><span id="L-259"><a href="#L-259"><span class="linenos"> 259</span></a><span class="sd">    - `verbose`: `bool`, Optional, determining level of information returned to the user</span>
</span><span id="L-260"><a href="#L-260"><span class="linenos"> 260</span></a><span class="sd">    - `debug`: `bool`, Optional, determining level of information logged on the server</span>
</span><span id="L-261"><a href="#L-261"><span class="linenos"> 261</span></a>
</span><span id="L-262"><a href="#L-262"><span class="linenos"> 262</span></a><span class="sd">    ## Returns</span>
</span><span id="L-263"><a href="#L-263"><span class="linenos"> 263</span></a>
</span><span id="L-264"><a href="#L-264"><span class="linenos"> 264</span></a><span class="sd">    - `list` of `str` dataset ids</span>
</span><span id="L-265"><a href="#L-265"><span class="linenos"> 265</span></a>
</span><span id="L-266"><a href="#L-266"><span class="linenos"> 266</span></a><span class="sd">    ## Example</span>
</span><span id="L-267"><a href="#L-267"><span class="linenos"> 267</span></a>
</span><span id="L-268"><a href="#L-268"><span class="linenos"> 268</span></a><span class="sd">    ```python</span>
</span><span id="L-269"><a href="#L-269"><span class="linenos"> 269</span></a><span class="sd">    import pandas as pd</span>
</span><span id="L-270"><a href="#L-270"><span class="linenos"> 270</span></a><span class="sd">    import twinlab as tl</span>
</span><span id="L-271"><a href="#L-271"><span class="linenos"> 271</span></a>
</span><span id="L-272"><a href="#L-272"><span class="linenos"> 272</span></a><span class="sd">    datasets = tl.list_datasets()</span>
</span><span id="L-273"><a href="#L-273"><span class="linenos"> 273</span></a><span class="sd">    print(datasets)</span>
</span><span id="L-274"><a href="#L-274"><span class="linenos"> 274</span></a><span class="sd">    ```</span>
</span><span id="L-275"><a href="#L-275"><span class="linenos"> 275</span></a><span class="sd">    &quot;&quot;&quot;</span>
</span><span id="L-276"><a href="#L-276"><span class="linenos"> 276</span></a>    <span class="n">response</span> <span class="o">=</span> <span class="n">api</span><span class="o">.</span><span class="n">list_datasets</span><span class="p">(</span><span class="n">verbose</span><span class="o">=</span><span class="n">debug</span><span class="p">)</span>
</span><span id="L-277"><a href="#L-277"><span class="linenos"> 277</span></a>    <span class="n">datasets</span> <span class="o">=</span> <span class="n">get_value_from_body</span><span class="p">(</span><span class="s2">&quot;datasets&quot;</span><span class="p">,</span> <span class="n">response</span><span class="p">)</span>
</span><span id="L-278"><a href="#L-278"><span class="linenos"> 278</span></a>    <span class="k">if</span> <span class="n">verbose</span><span class="p">:</span>
</span><span id="L-279"><a href="#L-279"><span class="linenos"> 279</span></a>        <span class="nb">print</span><span class="p">(</span><span class="s2">&quot;Datasets:&quot;</span><span class="p">)</span>
</span><span id="L-280"><a href="#L-280"><span class="linenos"> 280</span></a>        <span class="n">pprint</span><span class="p">(</span><span class="n">datasets</span><span class="p">,</span> <span class="n">compact</span><span class="o">=</span><span class="kc">True</span><span class="p">,</span> <span class="n">sort_dicts</span><span class="o">=</span><span class="kc">False</span><span class="p">)</span>
</span><span id="L-281"><a href="#L-281"><span class="linenos"> 281</span></a>    <span class="k">return</span> <span class="n">datasets</span>
</span><span id="L-282"><a href="#L-282"><span class="linenos"> 282</span></a>
</span><span id="L-283"><a href="#L-283"><span class="linenos"> 283</span></a>    <span class="c1"># try:</span>
</span><span id="L-284"><a href="#L-284"><span class="linenos"> 284</span></a>    <span class="c1">#     datasets = get_value_from_body(&quot;datasets&quot;, response)</span>
</span><span id="L-285"><a href="#L-285"><span class="linenos"> 285</span></a>    <span class="c1">#     if verbose:</span>
</span><span id="L-286"><a href="#L-286"><span class="linenos"> 286</span></a>    <span class="c1">#         print(&quot;Datasets:&quot;)</span>
</span><span id="L-287"><a href="#L-287"><span class="linenos"> 287</span></a>    <span class="c1">#         pprint(datasets, compact=True, sort_dicts=False)</span>
</span><span id="L-288"><a href="#L-288"><span class="linenos"> 288</span></a>    <span class="c1">#     return datasets</span>
</span><span id="L-289"><a href="#L-289"><span class="linenos"> 289</span></a>    <span class="c1"># except:</span>
</span><span id="L-290"><a href="#L-290"><span class="linenos"> 290</span></a>    <span class="c1">#     print(response)</span>
</span><span id="L-291"><a href="#L-291"><span class="linenos"> 291</span></a>
</span><span id="L-292"><a href="#L-292"><span class="linenos"> 292</span></a>
</span><span id="L-293"><a href="#L-293"><span class="linenos"> 293</span></a><span class="nd">@typechecked</span>
</span><span id="L-294"><a href="#L-294"><span class="linenos"> 294</span></a><span class="k">def</span> <span class="nf">view_dataset</span><span class="p">(</span>
</span><span id="L-295"><a href="#L-295"><span class="linenos"> 295</span></a>    <span class="n">dataset_id</span><span class="p">:</span> <span class="nb">str</span><span class="p">,</span> <span class="n">verbose</span><span class="p">:</span> <span class="n">Optional</span><span class="p">[</span><span class="nb">bool</span><span class="p">]</span> <span class="o">=</span> <span class="kc">False</span><span class="p">,</span> <span class="n">debug</span><span class="p">:</span> <span class="n">Optional</span><span class="p">[</span><span class="nb">bool</span><span class="p">]</span> <span class="o">=</span> <span class="kc">False</span>
</span><span id="L-296"><a href="#L-296"><span class="linenos"> 296</span></a><span class="p">)</span> <span class="o">-&gt;</span> <span class="n">pd</span><span class="o">.</span><span class="n">DataFrame</span><span class="p">:</span>
</span><span id="L-297"><a href="#L-297"><span class="linenos"> 297</span></a><span class="w">    </span><span class="sd">&quot;&quot;&quot;</span>
</span><span id="L-298"><a href="#L-298"><span class="linenos"> 298</span></a><span class="sd">    # View dataset</span>
</span><span id="L-299"><a href="#L-299"><span class="linenos"> 299</span></a>
</span><span id="L-300"><a href="#L-300"><span class="linenos"> 300</span></a><span class="sd">    View a dataset that exists on the twinLab cloud.</span>
</span><span id="L-301"><a href="#L-301"><span class="linenos"> 301</span></a>
</span><span id="L-302"><a href="#L-302"><span class="linenos"> 302</span></a><span class="sd">    ## Arguments</span>
</span><span id="L-303"><a href="#L-303"><span class="linenos"> 303</span></a>
</span><span id="L-304"><a href="#L-304"><span class="linenos"> 304</span></a><span class="sd">    - `dataset_id`: `str`; name for the dataset when saved to the twinLab cloud</span>
</span><span id="L-305"><a href="#L-305"><span class="linenos"> 305</span></a><span class="sd">    - `verbose`: `bool`, Optional, determining level of information returned to the user</span>
</span><span id="L-306"><a href="#L-306"><span class="linenos"> 306</span></a><span class="sd">    - `debug`: `bool`, Optional, determining level of information logged on the server</span>
</span><span id="L-307"><a href="#L-307"><span class="linenos"> 307</span></a>
</span><span id="L-308"><a href="#L-308"><span class="linenos"> 308</span></a><span class="sd">    ## Returns</span>
</span><span id="L-309"><a href="#L-309"><span class="linenos"> 309</span></a>
</span><span id="L-310"><a href="#L-310"><span class="linenos"> 310</span></a><span class="sd">    - `pandas.DataFrame` of the dataset.</span>
</span><span id="L-311"><a href="#L-311"><span class="linenos"> 311</span></a>
</span><span id="L-312"><a href="#L-312"><span class="linenos"> 312</span></a>
</span><span id="L-313"><a href="#L-313"><span class="linenos"> 313</span></a><span class="sd">    ## Example</span>
</span><span id="L-314"><a href="#L-314"><span class="linenos"> 314</span></a>
</span><span id="L-315"><a href="#L-315"><span class="linenos"> 315</span></a><span class="sd">    ```python</span>
</span><span id="L-316"><a href="#L-316"><span class="linenos"> 316</span></a><span class="sd">    import pandas as pd</span>
</span><span id="L-317"><a href="#L-317"><span class="linenos"> 317</span></a><span class="sd">    import twinlab as tl</span>
</span><span id="L-318"><a href="#L-318"><span class="linenos"> 318</span></a>
</span><span id="L-319"><a href="#L-319"><span class="linenos"> 319</span></a><span class="sd">    df = pd.DataFrame({&#39;X&#39;: [1, 2, 3, 4], &#39;y&#39;: [1, 4, 9, 16]})</span>
</span><span id="L-320"><a href="#L-320"><span class="linenos"> 320</span></a><span class="sd">    tl.upload_dataset(df, &quot;my_dataset&quot;)</span>
</span><span id="L-321"><a href="#L-321"><span class="linenos"> 321</span></a><span class="sd">    df = tl.view_dataset(&quot;my_dataset&quot;)</span>
</span><span id="L-322"><a href="#L-322"><span class="linenos"> 322</span></a><span class="sd">    print(df)</span>
</span><span id="L-323"><a href="#L-323"><span class="linenos"> 323</span></a><span class="sd">    ```</span>
</span><span id="L-324"><a href="#L-324"><span class="linenos"> 324</span></a><span class="sd">    &quot;&quot;&quot;</span>
</span><span id="L-325"><a href="#L-325"><span class="linenos"> 325</span></a>    <span class="n">response</span> <span class="o">=</span> <span class="n">api</span><span class="o">.</span><span class="n">view_dataset</span><span class="p">(</span><span class="n">dataset_id</span><span class="p">,</span> <span class="n">verbose</span><span class="o">=</span><span class="n">debug</span><span class="p">)</span>
</span><span id="L-326"><a href="#L-326"><span class="linenos"> 326</span></a>    <span class="n">csv_string</span> <span class="o">=</span> <span class="n">get_value_from_body</span><span class="p">(</span><span class="s2">&quot;dataset&quot;</span><span class="p">,</span> <span class="n">response</span><span class="p">)</span>
</span><span id="L-327"><a href="#L-327"><span class="linenos"> 327</span></a>    <span class="n">csv_string</span> <span class="o">=</span> <span class="n">io</span><span class="o">.</span><span class="n">StringIO</span><span class="p">(</span><span class="n">csv_string</span><span class="p">)</span>
</span><span id="L-328"><a href="#L-328"><span class="linenos"> 328</span></a>    <span class="n">df</span> <span class="o">=</span> <span class="n">pd</span><span class="o">.</span><span class="n">read_csv</span><span class="p">(</span><span class="n">csv_string</span><span class="p">,</span> <span class="n">sep</span><span class="o">=</span><span class="s2">&quot;,&quot;</span><span class="p">)</span>
</span><span id="L-329"><a href="#L-329"><span class="linenos"> 329</span></a>    <span class="k">if</span> <span class="n">verbose</span><span class="p">:</span>
</span><span id="L-330"><a href="#L-330"><span class="linenos"> 330</span></a>        <span class="nb">print</span><span class="p">(</span><span class="s2">&quot;Dataset:&quot;</span><span class="p">)</span>
</span><span id="L-331"><a href="#L-331"><span class="linenos"> 331</span></a>        <span class="nb">print</span><span class="p">(</span><span class="n">df</span><span class="p">)</span>
</span><span id="L-332"><a href="#L-332"><span class="linenos"> 332</span></a>    <span class="k">return</span> <span class="n">df</span>
</span><span id="L-333"><a href="#L-333"><span class="linenos"> 333</span></a>
</span><span id="L-334"><a href="#L-334"><span class="linenos"> 334</span></a>
</span><span id="L-335"><a href="#L-335"><span class="linenos"> 335</span></a><span class="nd">@typechecked</span>
</span><span id="L-336"><a href="#L-336"><span class="linenos"> 336</span></a><span class="k">def</span> <span class="nf">query_dataset</span><span class="p">(</span>
</span><span id="L-337"><a href="#L-337"><span class="linenos"> 337</span></a>    <span class="n">dataset_id</span><span class="p">:</span> <span class="nb">str</span><span class="p">,</span> <span class="n">verbose</span><span class="p">:</span> <span class="n">Optional</span><span class="p">[</span><span class="nb">bool</span><span class="p">]</span> <span class="o">=</span> <span class="kc">False</span><span class="p">,</span> <span class="n">debug</span><span class="p">:</span> <span class="n">Optional</span><span class="p">[</span><span class="nb">bool</span><span class="p">]</span> <span class="o">=</span> <span class="kc">False</span>
</span><span id="L-338"><a href="#L-338"><span class="linenos"> 338</span></a><span class="p">)</span> <span class="o">-&gt;</span> <span class="n">pd</span><span class="o">.</span><span class="n">DataFrame</span><span class="p">:</span>
</span><span id="L-339"><a href="#L-339"><span class="linenos"> 339</span></a><span class="w">    </span><span class="sd">&quot;&quot;&quot;</span>
</span><span id="L-340"><a href="#L-340"><span class="linenos"> 340</span></a><span class="sd">    # Query dataset</span>
</span><span id="L-341"><a href="#L-341"><span class="linenos"> 341</span></a>
</span><span id="L-342"><a href="#L-342"><span class="linenos"> 342</span></a><span class="sd">    Query a dataset that exists on the `twinLab` cloud by printing summary statistics.</span>
</span><span id="L-343"><a href="#L-343"><span class="linenos"> 343</span></a>
</span><span id="L-344"><a href="#L-344"><span class="linenos"> 344</span></a><span class="sd">    ## Arguments</span>
</span><span id="L-345"><a href="#L-345"><span class="linenos"> 345</span></a>
</span><span id="L-346"><a href="#L-346"><span class="linenos"> 346</span></a><span class="sd">    - `dataset_id`: `str`; name of dataset on S3 (same as the uploaded file name)</span>
</span><span id="L-347"><a href="#L-347"><span class="linenos"> 347</span></a><span class="sd">    - `verbose`: `bool`, Optional, determining level of information returned to the user</span>
</span><span id="L-348"><a href="#L-348"><span class="linenos"> 348</span></a><span class="sd">    - `debug`: `bool`, Optional, determining level of information logged on the server</span>
</span><span id="L-349"><a href="#L-349"><span class="linenos"> 349</span></a>
</span><span id="L-350"><a href="#L-350"><span class="linenos"> 350</span></a><span class="sd">    ## Returns</span>
</span><span id="L-351"><a href="#L-351"><span class="linenos"> 351</span></a>
</span><span id="L-352"><a href="#L-352"><span class="linenos"> 352</span></a><span class="sd">    - `pandas.DataFrame` containing summary statistics for the dataset.</span>
</span><span id="L-353"><a href="#L-353"><span class="linenos"> 353</span></a>
</span><span id="L-354"><a href="#L-354"><span class="linenos"> 354</span></a><span class="sd">    ## Example</span>
</span><span id="L-355"><a href="#L-355"><span class="linenos"> 355</span></a>
</span><span id="L-356"><a href="#L-356"><span class="linenos"> 356</span></a><span class="sd">    ```python</span>
</span><span id="L-357"><a href="#L-357"><span class="linenos"> 357</span></a><span class="sd">    import pandas as pd</span>
</span><span id="L-358"><a href="#L-358"><span class="linenos"> 358</span></a><span class="sd">    import twinlab as tl</span>
</span><span id="L-359"><a href="#L-359"><span class="linenos"> 359</span></a>
</span><span id="L-360"><a href="#L-360"><span class="linenos"> 360</span></a><span class="sd">    df = pd.DataFrame({&#39;X&#39;: [1, 2, 3, 4], &#39;y&#39;: [1, 4, 9, 16]})</span>
</span><span id="L-361"><a href="#L-361"><span class="linenos"> 361</span></a><span class="sd">    tl.upload_dataset(df, &quot;my_dataset&quot;)</span>
</span><span id="L-362"><a href="#L-362"><span class="linenos"> 362</span></a><span class="sd">    df = tl.query_dataset(&quot;my_dataset&quot;)</span>
</span><span id="L-363"><a href="#L-363"><span class="linenos"> 363</span></a><span class="sd">    print(df)</span>
</span><span id="L-364"><a href="#L-364"><span class="linenos"> 364</span></a><span class="sd">    ```</span>
</span><span id="L-365"><a href="#L-365"><span class="linenos"> 365</span></a><span class="sd">    &quot;&quot;&quot;</span>
</span><span id="L-366"><a href="#L-366"><span class="linenos"> 366</span></a>    <span class="n">response</span> <span class="o">=</span> <span class="n">api</span><span class="o">.</span><span class="n">summarise_dataset</span><span class="p">(</span><span class="n">dataset_id</span><span class="p">,</span> <span class="n">verbose</span><span class="o">=</span><span class="n">debug</span><span class="p">)</span>
</span><span id="L-367"><a href="#L-367"><span class="linenos"> 367</span></a>    <span class="n">csv_string</span> <span class="o">=</span> <span class="n">get_value_from_body</span><span class="p">(</span><span class="s2">&quot;dataset_summary&quot;</span><span class="p">,</span> <span class="n">response</span><span class="p">)</span>
</span><span id="L-368"><a href="#L-368"><span class="linenos"> 368</span></a>    <span class="n">csv_string</span> <span class="o">=</span> <span class="n">io</span><span class="o">.</span><span class="n">StringIO</span><span class="p">(</span><span class="n">csv_string</span><span class="p">)</span>
</span><span id="L-369"><a href="#L-369"><span class="linenos"> 369</span></a>    <span class="n">df</span> <span class="o">=</span> <span class="n">pd</span><span class="o">.</span><span class="n">read_csv</span><span class="p">(</span><span class="n">csv_string</span><span class="p">,</span> <span class="n">index_col</span><span class="o">=</span><span class="mi">0</span><span class="p">,</span> <span class="n">sep</span><span class="o">=</span><span class="s2">&quot;,&quot;</span><span class="p">)</span>
</span><span id="L-370"><a href="#L-370"><span class="linenos"> 370</span></a>    <span class="k">if</span> <span class="n">verbose</span><span class="p">:</span>
</span><span id="L-371"><a href="#L-371"><span class="linenos"> 371</span></a>        <span class="nb">print</span><span class="p">(</span><span class="s2">&quot;Dataset summary:&quot;</span><span class="p">)</span>
</span><span id="L-372"><a href="#L-372"><span class="linenos"> 372</span></a>        <span class="nb">print</span><span class="p">(</span><span class="n">df</span><span class="p">)</span>
</span><span id="L-373"><a href="#L-373"><span class="linenos"> 373</span></a>    <span class="k">return</span> <span class="n">df</span>
</span><span id="L-374"><a href="#L-374"><span class="linenos"> 374</span></a>
</span><span id="L-375"><a href="#L-375"><span class="linenos"> 375</span></a>
</span><span id="L-376"><a href="#L-376"><span class="linenos"> 376</span></a><span class="nd">@typechecked</span>
</span><span id="L-377"><a href="#L-377"><span class="linenos"> 377</span></a><span class="k">def</span> <span class="nf">delete_dataset</span><span class="p">(</span>
</span><span id="L-378"><a href="#L-378"><span class="linenos"> 378</span></a>    <span class="n">dataset_id</span><span class="p">:</span> <span class="nb">str</span><span class="p">,</span> <span class="n">verbose</span><span class="p">:</span> <span class="n">Optional</span><span class="p">[</span><span class="nb">bool</span><span class="p">]</span> <span class="o">=</span> <span class="kc">False</span><span class="p">,</span> <span class="n">debug</span><span class="p">:</span> <span class="n">Optional</span><span class="p">[</span><span class="nb">bool</span><span class="p">]</span> <span class="o">=</span> <span class="kc">False</span>
</span><span id="L-379"><a href="#L-379"><span class="linenos"> 379</span></a><span class="p">)</span> <span class="o">-&gt;</span> <span class="kc">None</span><span class="p">:</span>
</span><span id="L-380"><a href="#L-380"><span class="linenos"> 380</span></a><span class="w">    </span><span class="sd">&quot;&quot;&quot;</span>
</span><span id="L-381"><a href="#L-381"><span class="linenos"> 381</span></a><span class="sd">    # Delete dataset</span>
</span><span id="L-382"><a href="#L-382"><span class="linenos"> 382</span></a>
</span><span id="L-383"><a href="#L-383"><span class="linenos"> 383</span></a><span class="sd">    Delete a dataset from the `twinLab` cloud.</span>
</span><span id="L-384"><a href="#L-384"><span class="linenos"> 384</span></a>
</span><span id="L-385"><a href="#L-385"><span class="linenos"> 385</span></a><span class="sd">    ## Arguments</span>
</span><span id="L-386"><a href="#L-386"><span class="linenos"> 386</span></a>
</span><span id="L-387"><a href="#L-387"><span class="linenos"> 387</span></a><span class="sd">    - `dataset_id`: `str`; name of dataset to delete from the cloud</span>
</span><span id="L-388"><a href="#L-388"><span class="linenos"> 388</span></a><span class="sd">    - `verbose`: `bool`, Optional, determining level of information returned to the user</span>
</span><span id="L-389"><a href="#L-389"><span class="linenos"> 389</span></a><span class="sd">    - `debug`: `bool`, Optional, determining level of information logged on the server</span>
</span><span id="L-390"><a href="#L-390"><span class="linenos"> 390</span></a>
</span><span id="L-391"><a href="#L-391"><span class="linenos"> 391</span></a><span class="sd">    ## Example</span>
</span><span id="L-392"><a href="#L-392"><span class="linenos"> 392</span></a>
</span><span id="L-393"><a href="#L-393"><span class="linenos"> 393</span></a><span class="sd">    ```python</span>
</span><span id="L-394"><a href="#L-394"><span class="linenos"> 394</span></a><span class="sd">    import pandas as pd</span>
</span><span id="L-395"><a href="#L-395"><span class="linenos"> 395</span></a><span class="sd">    import twinlab as tl</span>
</span><span id="L-396"><a href="#L-396"><span class="linenos"> 396</span></a>
</span><span id="L-397"><a href="#L-397"><span class="linenos"> 397</span></a><span class="sd">    df = pd.DataFrame({&#39;X&#39;: [1, 2, 3, 4], &#39;y&#39;: [1, 4, 9, 16]})</span>
</span><span id="L-398"><a href="#L-398"><span class="linenos"> 398</span></a><span class="sd">    tl.upload_dataset(df, &quot;my_dataset&quot;)</span>
</span><span id="L-399"><a href="#L-399"><span class="linenos"> 399</span></a><span class="sd">    tl.delete_dataset(&quot;my_dataset&quot;)</span>
</span><span id="L-400"><a href="#L-400"><span class="linenos"> 400</span></a><span class="sd">    ```</span>
</span><span id="L-401"><a href="#L-401"><span class="linenos"> 401</span></a><span class="sd">    &quot;&quot;&quot;</span>
</span><span id="L-402"><a href="#L-402"><span class="linenos"> 402</span></a>    <span class="n">response</span> <span class="o">=</span> <span class="n">api</span><span class="o">.</span><span class="n">delete_dataset</span><span class="p">(</span><span class="n">dataset_id</span><span class="p">,</span> <span class="n">verbose</span><span class="o">=</span><span class="n">debug</span><span class="p">)</span>
</span><span id="L-403"><a href="#L-403"><span class="linenos"> 403</span></a>    <span class="k">if</span> <span class="n">verbose</span><span class="p">:</span>
</span><span id="L-404"><a href="#L-404"><span class="linenos"> 404</span></a>        <span class="n">message</span> <span class="o">=</span> <span class="n">_get_message</span><span class="p">(</span><span class="n">response</span><span class="p">)</span>
</span><span id="L-405"><a href="#L-405"><span class="linenos"> 405</span></a>        <span class="nb">print</span><span class="p">(</span><span class="n">message</span><span class="p">)</span>
</span><span id="L-406"><a href="#L-406"><span class="linenos"> 406</span></a>
</span><span id="L-407"><a href="#L-407"><span class="linenos"> 407</span></a>
</span><span id="L-408"><a href="#L-408"><span class="linenos"> 408</span></a><span class="c1">###  ###</span>
</span><span id="L-409"><a href="#L-409"><span class="linenos"> 409</span></a>
</span><span id="L-410"><a href="#L-410"><span class="linenos"> 410</span></a><span class="c1">### Campaign functions ###</span>
</span><span id="L-411"><a href="#L-411"><span class="linenos"> 411</span></a>
</span><span id="L-412"><a href="#L-412"><span class="linenos"> 412</span></a>
</span><span id="L-413"><a href="#L-413"><span class="linenos"> 413</span></a><span class="nd">@typechecked</span>
</span><span id="L-414"><a href="#L-414"><span class="linenos"> 414</span></a><span class="k">def</span> <span class="nf">train_campaign</span><span class="p">(</span>
</span><span id="L-415"><a href="#L-415"><span class="linenos"> 415</span></a>    <span class="n">filepath_or_params</span><span class="p">:</span> <span class="n">Union</span><span class="p">[</span><span class="nb">str</span><span class="p">,</span> <span class="nb">dict</span><span class="p">],</span>
</span><span id="L-416"><a href="#L-416"><span class="linenos"> 416</span></a>    <span class="n">campaign_id</span><span class="p">:</span> <span class="nb">str</span><span class="p">,</span>
</span><span id="L-417"><a href="#L-417"><span class="linenos"> 417</span></a>    <span class="n">ping_time</span><span class="p">:</span> <span class="n">Optional</span><span class="p">[</span><span class="nb">float</span><span class="p">]</span> <span class="o">=</span> <span class="mf">1.0</span><span class="p">,</span>
</span><span id="L-418"><a href="#L-418"><span class="linenos"> 418</span></a>    <span class="n">processor</span><span class="p">:</span> <span class="n">Optional</span><span class="p">[</span><span class="nb">str</span><span class="p">]</span> <span class="o">=</span> <span class="s2">&quot;cpu&quot;</span><span class="p">,</span>
</span><span id="L-419"><a href="#L-419"><span class="linenos"> 419</span></a>    <span class="n">verbose</span><span class="p">:</span> <span class="n">Optional</span><span class="p">[</span><span class="nb">bool</span><span class="p">]</span> <span class="o">=</span> <span class="kc">False</span><span class="p">,</span>
</span><span id="L-420"><a href="#L-420"><span class="linenos"> 420</span></a>    <span class="n">debug</span><span class="p">:</span> <span class="n">Optional</span><span class="p">[</span><span class="nb">bool</span><span class="p">]</span> <span class="o">=</span> <span class="kc">False</span><span class="p">,</span>
</span><span id="L-421"><a href="#L-421"><span class="linenos"> 421</span></a><span class="p">)</span> <span class="o">-&gt;</span> <span class="kc">None</span><span class="p">:</span>
</span><span id="L-422"><a href="#L-422"><span class="linenos"> 422</span></a><span class="w">    </span><span class="sd">&quot;&quot;&quot;</span>
</span><span id="L-423"><a href="#L-423"><span class="linenos"> 423</span></a><span class="sd">    # Train campaign</span>
</span><span id="L-424"><a href="#L-424"><span class="linenos"> 424</span></a>
</span><span id="L-425"><a href="#L-425"><span class="linenos"> 425</span></a><span class="sd">    Train a campaign in the `twinLab` cloud.</span>
</span><span id="L-426"><a href="#L-426"><span class="linenos"> 426</span></a>
</span><span id="L-427"><a href="#L-427"><span class="linenos"> 427</span></a><span class="sd">    ## Arguments</span>
</span><span id="L-428"><a href="#L-428"><span class="linenos"> 428</span></a>
</span><span id="L-429"><a href="#L-429"><span class="linenos"> 429</span></a><span class="sd">    - `filepath_or_params`: `str`, `dict`, Union; filepath to local json or parameters dictionary for training</span>
</span><span id="L-430"><a href="#L-430"><span class="linenos"> 430</span></a><span class="sd">    - `campaign_id`: `str`, name for the final trained campaign</span>
</span><span id="L-431"><a href="#L-431"><span class="linenos"> 431</span></a><span class="sd">    **Warning:** If the `campaign_id` already exists for the current cloud account, it will be overwritten by the</span>
</span><span id="L-432"><a href="#L-432"><span class="linenos"> 432</span></a><span class="sd">    newly trained campaign</span>
</span><span id="L-433"><a href="#L-433"><span class="linenos"> 433</span></a><span class="sd">    - `ping_time`: `float`, Optional, time between pings to the server to check if the job is complete [s]</span>
</span><span id="L-434"><a href="#L-434"><span class="linenos"> 434</span></a><span class="sd">    - `processor`: `str`, Optional, processor to use for sampling (&quot;cpu&quot;; &quot;gpu&quot;)</span>
</span><span id="L-435"><a href="#L-435"><span class="linenos"> 435</span></a><span class="sd">    - `verbose`: `bool`, Optional, determining level of information returned to the user</span>
</span><span id="L-436"><a href="#L-436"><span class="linenos"> 436</span></a><span class="sd">    - `debug`: `bool`, Optional, determining level of information logged on the server</span>
</span><span id="L-437"><a href="#L-437"><span class="linenos"> 437</span></a>
</span><span id="L-438"><a href="#L-438"><span class="linenos"> 438</span></a><span class="sd">    The parameters retrieved from the first argument are divided into 2 different sets of parameters, one for</span>
</span><span id="L-439"><a href="#L-439"><span class="linenos"> 439</span></a><span class="sd">    setting up the campaign and the other for training the campaign.</span>
</span><span id="L-440"><a href="#L-440"><span class="linenos"> 440</span></a>
</span><span id="L-441"><a href="#L-441"><span class="linenos"> 441</span></a><span class="sd">    Parameters to setup the campaign(used during initialization of a Campaign class object):</span>
</span><span id="L-442"><a href="#L-442"><span class="linenos"> 442</span></a><span class="sd">    - `dataset_id`: `str`, dataset_id of the dataset as stored in the cloud</span>
</span><span id="L-443"><a href="#L-443"><span class="linenos"> 443</span></a><span class="sd">    - `inputs`: `list`, a list of strings referring to the columns in the</span>
</span><span id="L-444"><a href="#L-444"><span class="linenos"> 444</span></a><span class="sd">                Pandas DataFrame that will be used as input parameters</span>
</span><span id="L-445"><a href="#L-445"><span class="linenos"> 445</span></a><span class="sd">    - `outputs`: `list`, a list of strings referring to the columns in the</span>
</span><span id="L-446"><a href="#L-446"><span class="linenos"> 446</span></a><span class="sd">                Pandas DataFrame that will be used as output parameters</span>
</span><span id="L-447"><a href="#L-447"><span class="linenos"> 447</span></a><span class="sd">    - `estimator`: `str`, Optional, The type of estimator used in the pipeline</span>
</span><span id="L-448"><a href="#L-448"><span class="linenos"> 448</span></a><span class="sd">                (&quot;gaussian_process_regression&quot; or &quot;gradient_boosting_regression&quot;)</span>
</span><span id="L-449"><a href="#L-449"><span class="linenos"> 449</span></a><span class="sd">    - `estimator_kwargs`: `dict`, Optional, keywords passed to the underlying estimator</span>
</span><span id="L-450"><a href="#L-450"><span class="linenos"> 450</span></a><span class="sd">                The estimator_kwargs dictionary for &quot;gaussian_process_regression&quot; allows the</span>
</span><span id="L-451"><a href="#L-451"><span class="linenos"> 451</span></a><span class="sd">                following keywords:</span>
</span><span id="L-452"><a href="#L-452"><span class="linenos"> 452</span></a><span class="sd">                `detrend`: `bool`, Optional, specifies whther to linear detrend the output</span>
</span><span id="L-453"><a href="#L-453"><span class="linenos"> 453</span></a><span class="sd">                        data before estimator fitting, default is False</span>
</span><span id="L-454"><a href="#L-454"><span class="linenos"> 454</span></a><span class="sd">                `device`: `str`, Optional, specifies whether to fit the estimator using</span>
</span><span id="L-455"><a href="#L-455"><span class="linenos"> 455</span></a><span class="sd">                        &quot;cpu&quot; or &quot;gpu&quot;, default is &quot;cpu&quot;</span>
</span><span id="L-456"><a href="#L-456"><span class="linenos"> 456</span></a><span class="sd">    - `decompose_input`: `bool`, Optional, specifies whether the input parameters</span>
</span><span id="L-457"><a href="#L-457"><span class="linenos"> 457</span></a><span class="sd">                should be decomposed</span>
</span><span id="L-458"><a href="#L-458"><span class="linenos"> 458</span></a><span class="sd">    - `input_explained_variance`: `float`, Optional, specifies how much of the</span>
</span><span id="L-459"><a href="#L-459"><span class="linenos"> 459</span></a><span class="sd">                variance should be explained after the truncation of the SVD</span>
</span><span id="L-460"><a href="#L-460"><span class="linenos"> 460</span></a><span class="sd">                (Singular Value Decomposition) for functional input</span>
</span><span id="L-461"><a href="#L-461"><span class="linenos"> 461</span></a><span class="sd">    - `decompose_output`: `bool`, Optional, specifies whether the output parameters</span>
</span><span id="L-462"><a href="#L-462"><span class="linenos"> 462</span></a><span class="sd">                should be decomposed</span>
</span><span id="L-463"><a href="#L-463"><span class="linenos"> 463</span></a><span class="sd">    - `output_explained_variance`: `float`, Optional, specifies how much of the</span>
</span><span id="L-464"><a href="#L-464"><span class="linenos"> 464</span></a><span class="sd">                variance should be explained after the truncation of the SVD</span>
</span><span id="L-465"><a href="#L-465"><span class="linenos"> 465</span></a><span class="sd">                (Singular Value Decomposition) for functional output</span>
</span><span id="L-466"><a href="#L-466"><span class="linenos"> 466</span></a>
</span><span id="L-467"><a href="#L-467"><span class="linenos"> 467</span></a><span class="sd">    Parameters to train the campaign(used when fit() function is called using a Campaign class object for training):</span>
</span><span id="L-468"><a href="#L-468"><span class="linenos"> 468</span></a><span class="sd">    - `train_test_ratio`: `float`, Optional, specifies the ratio of training samples in</span>
</span><span id="L-469"><a href="#L-469"><span class="linenos"> 469</span></a><span class="sd">            the dataset</span>
</span><span id="L-470"><a href="#L-470"><span class="linenos"> 470</span></a><span class="sd">    - `model_selection`: `bool`, Optional, whether to run model selection</span>
</span><span id="L-471"><a href="#L-471"><span class="linenos"> 471</span></a><span class="sd">    - `model_selection_kwargs`: `dict`, Optional, keywords passed to the model</span>
</span><span id="L-472"><a href="#L-472"><span class="linenos"> 472</span></a><span class="sd">            selection process</span>
</span><span id="L-473"><a href="#L-473"><span class="linenos"> 473</span></a><span class="sd">            The model_selection_kwargs dictionary for &quot;gaussian_process_regression&quot; allows the</span>
</span><span id="L-474"><a href="#L-474"><span class="linenos"> 474</span></a><span class="sd">            following keywords:</span>
</span><span id="L-475"><a href="#L-475"><span class="linenos"> 475</span></a><span class="sd">            `seed`: `int`, Optional, specifies the seed for the random number genrator for every</span>
</span><span id="L-476"><a href="#L-476"><span class="linenos"> 476</span></a><span class="sd">                trial of the model selection process</span>
</span><span id="L-477"><a href="#L-477"><span class="linenos"> 477</span></a><span class="sd">            `evaluation_metric`: `str`, Optional, specifies the evaluation metric used to score</span>
</span><span id="L-478"><a href="#L-478"><span class="linenos"> 478</span></a><span class="sd">                different configuration during the model selection process, can be &quot;BIC&quot; or &quot;MSLL&quot;,</span>
</span><span id="L-479"><a href="#L-479"><span class="linenos"> 479</span></a><span class="sd">                default is &quot;MSLL&quot;</span>
</span><span id="L-480"><a href="#L-480"><span class="linenos"> 480</span></a><span class="sd">            `val_ratio`: `float`, Optional, specifies the percentage of random validation data</span>
</span><span id="L-481"><a href="#L-481"><span class="linenos"> 481</span></a><span class="sd">                allocated to to compute the &quot;BIC&quot; metric, default is 0.2</span>
</span><span id="L-482"><a href="#L-482"><span class="linenos"> 482</span></a><span class="sd">            `base_kernels`: Set[str], Optional, specifies the list of kernels to use for</span>
</span><span id="L-483"><a href="#L-483"><span class="linenos"> 483</span></a><span class="sd">                Compositional Kernel Search, can be &quot;all&quot;, &quot;restricted&quot; or Set[str] object</span>
</span><span id="L-484"><a href="#L-484"><span class="linenos"> 484</span></a><span class="sd">                Set of available kernels are [&quot;LIN&quot;, &quot;M12&quot;, &quot;M32&quot;, &quot;M52&quot;, &quot;PER&quot;, &quot;RBF&quot;, &quot;RQF&quot;],</span>
</span><span id="L-485"><a href="#L-485"><span class="linenos"> 485</span></a><span class="sd">                default is &quot;restricted&quot; and uses [&quot;LIN&quot;, &quot;M32&quot;, &quot;M52&quot;, &quot;PER&quot;, &quot;RBF&quot;]</span>
</span><span id="L-486"><a href="#L-486"><span class="linenos"> 486</span></a><span class="sd">            `depth`: `int`, Optional, specifies the number of base kernels to be combined in</span>
</span><span id="L-487"><a href="#L-487"><span class="linenos"> 487</span></a><span class="sd">                the Compositional Kernel Search, depth=3 means the resulting kernel may be</span>
</span><span id="L-488"><a href="#L-488"><span class="linenos"> 488</span></a><span class="sd">                composed from three base kernels, e.g. &quot;(LIN+PER)*RBF&quot; or &quot;(M12*RBF)+RQF&quot;,</span>
</span><span id="L-489"><a href="#L-489"><span class="linenos"> 489</span></a><span class="sd">                default is 1</span>
</span><span id="L-490"><a href="#L-490"><span class="linenos"> 490</span></a><span class="sd">            `beam`: `int`, Optional, specifies the beam width of the Compositional Kernel Search</span>
</span><span id="L-491"><a href="#L-491"><span class="linenos"> 491</span></a><span class="sd">                algorithm, beam=1 is greedy search, beam=None performs breadth-first search and</span>
</span><span id="L-492"><a href="#L-492"><span class="linenos"> 492</span></a><span class="sd">                beam&gt;1 perfroms beam search with the specified beam value, default is None</span>
</span><span id="L-493"><a href="#L-493"><span class="linenos"> 493</span></a><span class="sd">            `resources_per_trial`: `dict`, Optional, The amount of CPU and GPU resources allocated</span>
</span><span id="L-494"><a href="#L-494"><span class="linenos"> 494</span></a><span class="sd">                to each trial of model selection, default is {&quot;cpu&quot;: 1, &quot;gpu&quot;: 0}</span>
</span><span id="L-495"><a href="#L-495"><span class="linenos"> 495</span></a><span class="sd">    - `seed`: `int`, Optional, specifies the seed for the random number generator</span>
</span><span id="L-496"><a href="#L-496"><span class="linenos"> 496</span></a>
</span><span id="L-497"><a href="#L-497"><span class="linenos"> 497</span></a><span class="sd">    ## Example</span>
</span><span id="L-498"><a href="#L-498"><span class="linenos"> 498</span></a>
</span><span id="L-499"><a href="#L-499"><span class="linenos"> 499</span></a><span class="sd">    Train using a local `json` parameters file:</span>
</span><span id="L-500"><a href="#L-500"><span class="linenos"> 500</span></a>
</span><span id="L-501"><a href="#L-501"><span class="linenos"> 501</span></a><span class="sd">    ```python</span>
</span><span id="L-502"><a href="#L-502"><span class="linenos"> 502</span></a><span class="sd">    import twinlab as tl</span>
</span><span id="L-503"><a href="#L-503"><span class="linenos"> 503</span></a>
</span><span id="L-504"><a href="#L-504"><span class="linenos"> 504</span></a><span class="sd">    tl.train_campaign(&quot;path/to/params.json&quot;, &quot;my_campaign&quot;)</span>
</span><span id="L-505"><a href="#L-505"><span class="linenos"> 505</span></a><span class="sd">    ```</span>
</span><span id="L-506"><a href="#L-506"><span class="linenos"> 506</span></a>
</span><span id="L-507"><a href="#L-507"><span class="linenos"> 507</span></a><span class="sd">    Train via a `python` dictionary:</span>
</span><span id="L-508"><a href="#L-508"><span class="linenos"> 508</span></a>
</span><span id="L-509"><a href="#L-509"><span class="linenos"> 509</span></a><span class="sd">    ```python</span>
</span><span id="L-510"><a href="#L-510"><span class="linenos"> 510</span></a><span class="sd">    import pandas as pd</span>
</span><span id="L-511"><a href="#L-511"><span class="linenos"> 511</span></a><span class="sd">    import twinlab as tl</span>
</span><span id="L-512"><a href="#L-512"><span class="linenos"> 512</span></a>
</span><span id="L-513"><a href="#L-513"><span class="linenos"> 513</span></a><span class="sd">    df = pd.DataFrame({&#39;X&#39;: [1, 2, 3, 4], &#39;y&#39;: [1, 4, 9, 16]})</span>
</span><span id="L-514"><a href="#L-514"><span class="linenos"> 514</span></a><span class="sd">    tl.upload_dataset(df, &quot;my_dataset&quot;)</span>
</span><span id="L-515"><a href="#L-515"><span class="linenos"> 515</span></a><span class="sd">    params = {</span>
</span><span id="L-516"><a href="#L-516"><span class="linenos"> 516</span></a><span class="sd">        &quot;dataset_id&quot;: &quot;my_dataset&quot;,</span>
</span><span id="L-517"><a href="#L-517"><span class="linenos"> 517</span></a><span class="sd">        &quot;inputs&quot;: [&quot;X&quot;],</span>
</span><span id="L-518"><a href="#L-518"><span class="linenos"> 518</span></a><span class="sd">        &quot;outputs&quot;: [&quot;y&quot;],</span>
</span><span id="L-519"><a href="#L-519"><span class="linenos"> 519</span></a><span class="sd">    }</span>
</span><span id="L-520"><a href="#L-520"><span class="linenos"> 520</span></a><span class="sd">    tl.train_campaign(params, &quot;my_campaign&quot;)</span>
</span><span id="L-521"><a href="#L-521"><span class="linenos"> 521</span></a><span class="sd">    ```</span>
</span><span id="L-522"><a href="#L-522"><span class="linenos"> 522</span></a><span class="sd">    &quot;&quot;&quot;</span>
</span><span id="L-523"><a href="#L-523"><span class="linenos"> 523</span></a>    <span class="k">if</span> <span class="nb">type</span><span class="p">(</span><span class="n">filepath_or_params</span><span class="p">)</span> <span class="ow">is</span> <span class="nb">dict</span><span class="p">:</span>
</span><span id="L-524"><a href="#L-524"><span class="linenos"> 524</span></a>        <span class="n">params</span> <span class="o">=</span> <span class="n">filepath_or_params</span>
</span><span id="L-525"><a href="#L-525"><span class="linenos"> 525</span></a>    <span class="k">elif</span> <span class="nb">type</span><span class="p">(</span><span class="n">filepath_or_params</span><span class="p">)</span> <span class="ow">is</span> <span class="nb">str</span><span class="p">:</span>
</span><span id="L-526"><a href="#L-526"><span class="linenos"> 526</span></a>        <span class="n">filepath</span> <span class="o">=</span> <span class="n">filepath_or_params</span>
</span><span id="L-527"><a href="#L-527"><span class="linenos"> 527</span></a>        <span class="n">params</span> <span class="o">=</span> <span class="n">json</span><span class="o">.</span><span class="n">load</span><span class="p">(</span><span class="nb">open</span><span class="p">(</span><span class="n">filepath</span><span class="p">))</span>
</span><span id="L-528"><a href="#L-528"><span class="linenos"> 528</span></a>    <span class="k">else</span><span class="p">:</span>
</span><span id="L-529"><a href="#L-529"><span class="linenos"> 529</span></a>        <span class="nb">print</span><span class="p">(</span><span class="s2">&quot;Type:&quot;</span><span class="p">,</span> <span class="nb">type</span><span class="p">(</span><span class="n">filepath_or_params</span><span class="p">))</span>
</span><span id="L-530"><a href="#L-530"><span class="linenos"> 530</span></a>        <span class="k">raise</span> <span class="ne">ValueError</span><span class="p">(</span><span class="s2">&quot;filepath_or_params must be either a string or a dictionary&quot;</span><span class="p">)</span>
</span><span id="L-531"><a href="#L-531"><span class="linenos"> 531</span></a>    <span class="n">params</span> <span class="o">=</span> <span class="n">utils</span><span class="o">.</span><span class="n">coerce_params_dict</span><span class="p">(</span><span class="n">params</span><span class="p">)</span>
</span><span id="L-532"><a href="#L-532"><span class="linenos"> 532</span></a>    <span class="n">params_str</span> <span class="o">=</span> <span class="n">json</span><span class="o">.</span><span class="n">dumps</span><span class="p">(</span><span class="n">params</span><span class="p">)</span>
</span><span id="L-533"><a href="#L-533"><span class="linenos"> 533</span></a>    <span class="n">response</span> <span class="o">=</span> <span class="n">api</span><span class="o">.</span><span class="n">train_model</span><span class="p">(</span>
</span><span id="L-534"><a href="#L-534"><span class="linenos"> 534</span></a>        <span class="n">campaign_id</span><span class="p">,</span> <span class="n">params_str</span><span class="p">,</span> <span class="n">processor</span><span class="o">=</span><span class="n">processor</span><span class="p">,</span> <span class="n">verbose</span><span class="o">=</span><span class="n">debug</span>
</span><span id="L-535"><a href="#L-535"><span class="linenos"> 535</span></a>    <span class="p">)</span>
</span><span id="L-536"><a href="#L-536"><span class="linenos"> 536</span></a>    <span class="k">if</span> <span class="n">verbose</span><span class="p">:</span>
</span><span id="L-537"><a href="#L-537"><span class="linenos"> 537</span></a>        <span class="n">message</span> <span class="o">=</span> <span class="n">_get_message</span><span class="p">(</span><span class="n">response</span><span class="p">)</span>
</span><span id="L-538"><a href="#L-538"><span class="linenos"> 538</span></a>        <span class="nb">print</span><span class="p">(</span><span class="n">message</span><span class="p">)</span>
</span><span id="L-539"><a href="#L-539"><span class="linenos"> 539</span></a>
</span><span id="L-540"><a href="#L-540"><span class="linenos"> 540</span></a>    <span class="c1"># Wait for job to complete</span>
</span><span id="L-541"><a href="#L-541"><span class="linenos"> 541</span></a>    <span class="n">complete</span> <span class="o">=</span> <span class="kc">False</span>
</span><span id="L-542"><a href="#L-542"><span class="linenos"> 542</span></a>    <span class="k">while</span> <span class="ow">not</span> <span class="n">complete</span><span class="p">:</span>
</span><span id="L-543"><a href="#L-543"><span class="linenos"> 543</span></a>        <span class="n">status</span> <span class="o">=</span> <span class="n">_status_campaign</span><span class="p">(</span><span class="n">campaign_id</span><span class="p">,</span> <span class="n">verbose</span><span class="o">=</span><span class="kc">False</span><span class="p">,</span> <span class="n">debug</span><span class="o">=</span><span class="n">debug</span><span class="p">)</span>
</span><span id="L-544"><a href="#L-544"><span class="linenos"> 544</span></a>        <span class="n">complete</span> <span class="o">=</span> <span class="n">get_value_from_body</span><span class="p">(</span><span class="s2">&quot;job_complete&quot;</span><span class="p">,</span> <span class="n">status</span><span class="p">)</span>
</span><span id="L-545"><a href="#L-545"><span class="linenos"> 545</span></a>        <span class="n">time</span><span class="o">.</span><span class="n">sleep</span><span class="p">(</span><span class="n">ping_time</span><span class="p">)</span>
</span><span id="L-546"><a href="#L-546"><span class="linenos"> 546</span></a>
</span><span id="L-547"><a href="#L-547"><span class="linenos"> 547</span></a>
</span><span id="L-548"><a href="#L-548"><span class="linenos"> 548</span></a><span class="nd">@typechecked</span>
</span><span id="L-549"><a href="#L-549"><span class="linenos"> 549</span></a><span class="k">def</span> <span class="nf">list_campaigns</span><span class="p">(</span>
</span><span id="L-550"><a href="#L-550"><span class="linenos"> 550</span></a>    <span class="n">verbose</span><span class="p">:</span> <span class="n">Optional</span><span class="p">[</span><span class="nb">bool</span><span class="p">]</span> <span class="o">=</span> <span class="kc">False</span><span class="p">,</span> <span class="n">debug</span><span class="p">:</span> <span class="n">Optional</span><span class="p">[</span><span class="nb">bool</span><span class="p">]</span> <span class="o">=</span> <span class="kc">False</span>
</span><span id="L-551"><a href="#L-551"><span class="linenos"> 551</span></a><span class="p">)</span> <span class="o">-&gt;</span> <span class="nb">list</span><span class="p">:</span>
</span><span id="L-552"><a href="#L-552"><span class="linenos"> 552</span></a><span class="w">    </span><span class="sd">&quot;&quot;&quot;</span>
</span><span id="L-553"><a href="#L-553"><span class="linenos"> 553</span></a><span class="sd">    # List campaigns</span>
</span><span id="L-554"><a href="#L-554"><span class="linenos"> 554</span></a>
</span><span id="L-555"><a href="#L-555"><span class="linenos"> 555</span></a><span class="sd">    List campaigns that have been completed to the `twinLab` cloud.</span>
</span><span id="L-556"><a href="#L-556"><span class="linenos"> 556</span></a>
</span><span id="L-557"><a href="#L-557"><span class="linenos"> 557</span></a><span class="sd">    ## Arguments</span>
</span><span id="L-558"><a href="#L-558"><span class="linenos"> 558</span></a>
</span><span id="L-559"><a href="#L-559"><span class="linenos"> 559</span></a><span class="sd">    - `verbose`: `bool`, Optional,determining level of information returned to the user</span>
</span><span id="L-560"><a href="#L-560"><span class="linenos"> 560</span></a><span class="sd">    - `debug`: `bool`, Optional, determining level of information logged on the server</span>
</span><span id="L-561"><a href="#L-561"><span class="linenos"> 561</span></a>
</span><span id="L-562"><a href="#L-562"><span class="linenos"> 562</span></a><span class="sd">    ## Returns</span>
</span><span id="L-563"><a href="#L-563"><span class="linenos"> 563</span></a>
</span><span id="L-564"><a href="#L-564"><span class="linenos"> 564</span></a><span class="sd">    - A `list` of `str` campaign ids</span>
</span><span id="L-565"><a href="#L-565"><span class="linenos"> 565</span></a>
</span><span id="L-566"><a href="#L-566"><span class="linenos"> 566</span></a><span class="sd">    ## Example</span>
</span><span id="L-567"><a href="#L-567"><span class="linenos"> 567</span></a>
</span><span id="L-568"><a href="#L-568"><span class="linenos"> 568</span></a><span class="sd">    ```python</span>
</span><span id="L-569"><a href="#L-569"><span class="linenos"> 569</span></a><span class="sd">    import twinlab as tl</span>
</span><span id="L-570"><a href="#L-570"><span class="linenos"> 570</span></a>
</span><span id="L-571"><a href="#L-571"><span class="linenos"> 571</span></a><span class="sd">    campaigns = tl.list_campaigns()</span>
</span><span id="L-572"><a href="#L-572"><span class="linenos"> 572</span></a><span class="sd">    print(campaigns)</span>
</span><span id="L-573"><a href="#L-573"><span class="linenos"> 573</span></a><span class="sd">    ```</span>
</span><span id="L-574"><a href="#L-574"><span class="linenos"> 574</span></a><span class="sd">    &quot;&quot;&quot;</span>
</span><span id="L-575"><a href="#L-575"><span class="linenos"> 575</span></a>    <span class="n">response</span> <span class="o">=</span> <span class="n">api</span><span class="o">.</span><span class="n">list_models</span><span class="p">(</span><span class="n">verbose</span><span class="o">=</span><span class="n">debug</span><span class="p">)</span>
</span><span id="L-576"><a href="#L-576"><span class="linenos"> 576</span></a>    <span class="n">campaigns</span> <span class="o">=</span> <span class="n">get_value_from_body</span><span class="p">(</span><span class="s2">&quot;models&quot;</span><span class="p">,</span> <span class="n">response</span><span class="p">)</span>
</span><span id="L-577"><a href="#L-577"><span class="linenos"> 577</span></a>    <span class="k">if</span> <span class="n">verbose</span><span class="p">:</span>
</span><span id="L-578"><a href="#L-578"><span class="linenos"> 578</span></a>        <span class="nb">print</span><span class="p">(</span><span class="s2">&quot;Trained models:&quot;</span><span class="p">)</span>
</span><span id="L-579"><a href="#L-579"><span class="linenos"> 579</span></a>        <span class="n">pprint</span><span class="p">(</span><span class="n">campaigns</span><span class="p">,</span> <span class="n">compact</span><span class="o">=</span><span class="kc">True</span><span class="p">,</span> <span class="n">sort_dicts</span><span class="o">=</span><span class="kc">False</span><span class="p">)</span>
</span><span id="L-580"><a href="#L-580"><span class="linenos"> 580</span></a>    <span class="k">return</span> <span class="n">campaigns</span>
</span><span id="L-581"><a href="#L-581"><span class="linenos"> 581</span></a>
</span><span id="L-582"><a href="#L-582"><span class="linenos"> 582</span></a>
</span><span id="L-583"><a href="#L-583"><span class="linenos"> 583</span></a><span class="nd">@typechecked</span>
</span><span id="L-584"><a href="#L-584"><span class="linenos"> 584</span></a><span class="k">def</span> <span class="nf">view_campaign</span><span class="p">(</span>
</span><span id="L-585"><a href="#L-585"><span class="linenos"> 585</span></a>    <span class="n">campaign_id</span><span class="p">:</span> <span class="nb">str</span><span class="p">,</span> <span class="n">verbose</span><span class="p">:</span> <span class="n">Optional</span><span class="p">[</span><span class="nb">bool</span><span class="p">]</span> <span class="o">=</span> <span class="kc">False</span><span class="p">,</span> <span class="n">debug</span><span class="p">:</span> <span class="n">Optional</span><span class="p">[</span><span class="nb">bool</span><span class="p">]</span> <span class="o">=</span> <span class="kc">False</span>
</span><span id="L-586"><a href="#L-586"><span class="linenos"> 586</span></a><span class="p">)</span> <span class="o">-&gt;</span> <span class="nb">dict</span><span class="p">:</span>
</span><span id="L-587"><a href="#L-587"><span class="linenos"> 587</span></a><span class="w">    </span><span class="sd">&quot;&quot;&quot;</span>
</span><span id="L-588"><a href="#L-588"><span class="linenos"> 588</span></a><span class="sd">    # View campaign</span>
</span><span id="L-589"><a href="#L-589"><span class="linenos"> 589</span></a>
</span><span id="L-590"><a href="#L-590"><span class="linenos"> 590</span></a><span class="sd">    View a campaign that exists on the twinLab cloud.</span>
</span><span id="L-591"><a href="#L-591"><span class="linenos"> 591</span></a>
</span><span id="L-592"><a href="#L-592"><span class="linenos"> 592</span></a><span class="sd">    ## Arguments</span>
</span><span id="L-593"><a href="#L-593"><span class="linenos"> 593</span></a>
</span><span id="L-594"><a href="#L-594"><span class="linenos"> 594</span></a><span class="sd">    - `campaign_id`: `str`; name for the model when saved to the twinLab cloud</span>
</span><span id="L-595"><a href="#L-595"><span class="linenos"> 595</span></a><span class="sd">    - `verbose`: `bool`, Optional, determining level of information returned to the user</span>
</span><span id="L-596"><a href="#L-596"><span class="linenos"> 596</span></a><span class="sd">    - `debug`: `bool`, Optional, determining level of information logged on the server</span>
</span><span id="L-597"><a href="#L-597"><span class="linenos"> 597</span></a>
</span><span id="L-598"><a href="#L-598"><span class="linenos"> 598</span></a><span class="sd">    ## Returns</span>
</span><span id="L-599"><a href="#L-599"><span class="linenos"> 599</span></a>
</span><span id="L-600"><a href="#L-600"><span class="linenos"> 600</span></a><span class="sd">    - `dict` containing the campaign training parameters.</span>
</span><span id="L-601"><a href="#L-601"><span class="linenos"> 601</span></a>
</span><span id="L-602"><a href="#L-602"><span class="linenos"> 602</span></a><span class="sd">    ## Example</span>
</span><span id="L-603"><a href="#L-603"><span class="linenos"> 603</span></a>
</span><span id="L-604"><a href="#L-604"><span class="linenos"> 604</span></a><span class="sd">    ```python</span>
</span><span id="L-605"><a href="#L-605"><span class="linenos"> 605</span></a><span class="sd">    import pandas as pd</span>
</span><span id="L-606"><a href="#L-606"><span class="linenos"> 606</span></a><span class="sd">    import twinlab as tl</span>
</span><span id="L-607"><a href="#L-607"><span class="linenos"> 607</span></a>
</span><span id="L-608"><a href="#L-608"><span class="linenos"> 608</span></a><span class="sd">    df = pd.DataFrame({&#39;X&#39;: [1, 2, 3, 4], &#39;y&#39;: [1, 4, 9, 16]})</span>
</span><span id="L-609"><a href="#L-609"><span class="linenos"> 609</span></a><span class="sd">    tl.upload_dataset(df, &quot;my_dataset&quot;)</span>
</span><span id="L-610"><a href="#L-610"><span class="linenos"> 610</span></a><span class="sd">    params = {</span>
</span><span id="L-611"><a href="#L-611"><span class="linenos"> 611</span></a><span class="sd">        &quot;dataset_id&quot;: &quot;my_dataset&quot;,</span>
</span><span id="L-612"><a href="#L-612"><span class="linenos"> 612</span></a><span class="sd">        &quot;inputs&quot;: [&quot;X&quot;],</span>
</span><span id="L-613"><a href="#L-613"><span class="linenos"> 613</span></a><span class="sd">        &quot;outputs&quot;: [&quot;y&quot;],</span>
</span><span id="L-614"><a href="#L-614"><span class="linenos"> 614</span></a><span class="sd">    }</span>
</span><span id="L-615"><a href="#L-615"><span class="linenos"> 615</span></a><span class="sd">    tl.train_campaign(params, &quot;my_campaign&quot;)</span>
</span><span id="L-616"><a href="#L-616"><span class="linenos"> 616</span></a><span class="sd">    params = tl.view_campaign(&quot;my_campaign&quot;)</span>
</span><span id="L-617"><a href="#L-617"><span class="linenos"> 617</span></a><span class="sd">    print(params)</span>
</span><span id="L-618"><a href="#L-618"><span class="linenos"> 618</span></a><span class="sd">    ```</span>
</span><span id="L-619"><a href="#L-619"><span class="linenos"> 619</span></a><span class="sd">    &quot;&quot;&quot;</span>
</span><span id="L-620"><a href="#L-620"><span class="linenos"> 620</span></a>    <span class="n">response</span> <span class="o">=</span> <span class="n">api</span><span class="o">.</span><span class="n">view_model</span><span class="p">(</span><span class="n">campaign_id</span><span class="p">,</span> <span class="n">verbose</span><span class="o">=</span><span class="n">debug</span><span class="p">)</span>
</span><span id="L-621"><a href="#L-621"><span class="linenos"> 621</span></a>    <span class="n">model_parameters</span> <span class="o">=</span> <span class="n">response</span>
</span><span id="L-622"><a href="#L-622"><span class="linenos"> 622</span></a>    <span class="k">if</span> <span class="n">verbose</span><span class="p">:</span>
</span><span id="L-623"><a href="#L-623"><span class="linenos"> 623</span></a>        <span class="nb">print</span><span class="p">(</span><span class="s2">&quot;Campaign summary:&quot;</span><span class="p">)</span>
</span><span id="L-624"><a href="#L-624"><span class="linenos"> 624</span></a>        <span class="n">pprint</span><span class="p">(</span><span class="n">model_parameters</span><span class="p">,</span> <span class="n">compact</span><span class="o">=</span><span class="kc">True</span><span class="p">,</span> <span class="n">sort_dicts</span><span class="o">=</span><span class="kc">False</span><span class="p">)</span>
</span><span id="L-625"><a href="#L-625"><span class="linenos"> 625</span></a>    <span class="k">return</span> <span class="n">model_parameters</span>
</span><span id="L-626"><a href="#L-626"><span class="linenos"> 626</span></a>
</span><span id="L-627"><a href="#L-627"><span class="linenos"> 627</span></a>
</span><span id="L-628"><a href="#L-628"><span class="linenos"> 628</span></a><span class="nd">@typechecked</span>
</span><span id="L-629"><a href="#L-629"><span class="linenos"> 629</span></a><span class="k">def</span> <span class="nf">query_campaign</span><span class="p">(</span>
</span><span id="L-630"><a href="#L-630"><span class="linenos"> 630</span></a>    <span class="n">campaign_id</span><span class="p">:</span> <span class="nb">str</span><span class="p">,</span> <span class="n">verbose</span><span class="p">:</span> <span class="n">Optional</span><span class="p">[</span><span class="nb">bool</span><span class="p">]</span> <span class="o">=</span> <span class="kc">False</span><span class="p">,</span> <span class="n">debug</span><span class="p">:</span> <span class="n">Optional</span><span class="p">[</span><span class="nb">bool</span><span class="p">]</span> <span class="o">=</span> <span class="kc">False</span>
</span><span id="L-631"><a href="#L-631"><span class="linenos"> 631</span></a><span class="p">)</span> <span class="o">-&gt;</span> <span class="nb">dict</span><span class="p">:</span>
</span><span id="L-632"><a href="#L-632"><span class="linenos"> 632</span></a><span class="w">    </span><span class="sd">&quot;&quot;&quot;</span>
</span><span id="L-633"><a href="#L-633"><span class="linenos"> 633</span></a><span class="sd">    # Query campaign</span>
</span><span id="L-634"><a href="#L-634"><span class="linenos"> 634</span></a>
</span><span id="L-635"><a href="#L-635"><span class="linenos"> 635</span></a><span class="sd">    Get summary statistics for a pre-trained campaign in the `twinLab` cloud.</span>
</span><span id="L-636"><a href="#L-636"><span class="linenos"> 636</span></a>
</span><span id="L-637"><a href="#L-637"><span class="linenos"> 637</span></a><span class="sd">    ## Arguments</span>
</span><span id="L-638"><a href="#L-638"><span class="linenos"> 638</span></a>
</span><span id="L-639"><a href="#L-639"><span class="linenos"> 639</span></a><span class="sd">    - `campaign_id`: `str`; name of trained campaign to query</span>
</span><span id="L-640"><a href="#L-640"><span class="linenos"> 640</span></a><span class="sd">    - `verbose`: `bool`, Optional, determining level of information returned to the user</span>
</span><span id="L-641"><a href="#L-641"><span class="linenos"> 641</span></a><span class="sd">    - `debug`: `bool`, Optional, determining level of information logged on the server</span>
</span><span id="L-642"><a href="#L-642"><span class="linenos"> 642</span></a>
</span><span id="L-643"><a href="#L-643"><span class="linenos"> 643</span></a><span class="sd">    ## Returns</span>
</span><span id="L-644"><a href="#L-644"><span class="linenos"> 644</span></a>
</span><span id="L-645"><a href="#L-645"><span class="linenos"> 645</span></a><span class="sd">    - `dict` containing summary statistics for the pre-trained campaign.</span>
</span><span id="L-646"><a href="#L-646"><span class="linenos"> 646</span></a>
</span><span id="L-647"><a href="#L-647"><span class="linenos"> 647</span></a><span class="sd">    ## Example</span>
</span><span id="L-648"><a href="#L-648"><span class="linenos"> 648</span></a>
</span><span id="L-649"><a href="#L-649"><span class="linenos"> 649</span></a><span class="sd">    ```python</span>
</span><span id="L-650"><a href="#L-650"><span class="linenos"> 650</span></a><span class="sd">    import pandas as pd</span>
</span><span id="L-651"><a href="#L-651"><span class="linenos"> 651</span></a><span class="sd">    import twinlab as tl</span>
</span><span id="L-652"><a href="#L-652"><span class="linenos"> 652</span></a>
</span><span id="L-653"><a href="#L-653"><span class="linenos"> 653</span></a><span class="sd">    df = pd.DataFrame({&#39;X&#39;: [1, 2, 3, 4], &#39;y&#39;: [1, 4, 9, 16]})</span>
</span><span id="L-654"><a href="#L-654"><span class="linenos"> 654</span></a><span class="sd">    tl.upload_dataset(df, &quot;my_dataset&quot;)</span>
</span><span id="L-655"><a href="#L-655"><span class="linenos"> 655</span></a><span class="sd">    params = {</span>
</span><span id="L-656"><a href="#L-656"><span class="linenos"> 656</span></a><span class="sd">        &quot;dataset_id&quot;: &quot;my_dataset&quot;,</span>
</span><span id="L-657"><a href="#L-657"><span class="linenos"> 657</span></a><span class="sd">        &quot;inputs&quot;: [&quot;X&quot;],</span>
</span><span id="L-658"><a href="#L-658"><span class="linenos"> 658</span></a><span class="sd">        &quot;outputs&quot;: [&quot;y&quot;],</span>
</span><span id="L-659"><a href="#L-659"><span class="linenos"> 659</span></a><span class="sd">    }</span>
</span><span id="L-660"><a href="#L-660"><span class="linenos"> 660</span></a><span class="sd">    tl.train_campaign(params, &quot;my_campaign&quot;)</span>
</span><span id="L-661"><a href="#L-661"><span class="linenos"> 661</span></a><span class="sd">    info = tl.query_campaign(&quot;my_campaign&quot;)</span>
</span><span id="L-662"><a href="#L-662"><span class="linenos"> 662</span></a><span class="sd">    print(info)</span>
</span><span id="L-663"><a href="#L-663"><span class="linenos"> 663</span></a><span class="sd">    ```</span>
</span><span id="L-664"><a href="#L-664"><span class="linenos"> 664</span></a><span class="sd">    &quot;&quot;&quot;</span>
</span><span id="L-665"><a href="#L-665"><span class="linenos"> 665</span></a>    <span class="n">response</span> <span class="o">=</span> <span class="n">api</span><span class="o">.</span><span class="n">summarise_model</span><span class="p">(</span><span class="n">campaign_id</span><span class="p">,</span> <span class="n">verbose</span><span class="o">=</span><span class="n">debug</span><span class="p">)</span>
</span><span id="L-666"><a href="#L-666"><span class="linenos"> 666</span></a>    <span class="n">summary</span> <span class="o">=</span> <span class="n">response</span>
</span><span id="L-667"><a href="#L-667"><span class="linenos"> 667</span></a>    <span class="c1"># summary = json.loads(response[&quot;model_summary&quot;]) # TODO: This should work eventually</span>
</span><span id="L-668"><a href="#L-668"><span class="linenos"> 668</span></a>    <span class="k">if</span> <span class="n">verbose</span><span class="p">:</span>
</span><span id="L-669"><a href="#L-669"><span class="linenos"> 669</span></a>        <span class="nb">print</span><span class="p">(</span><span class="s2">&quot;Model summary:&quot;</span><span class="p">)</span>
</span><span id="L-670"><a href="#L-670"><span class="linenos"> 670</span></a>        <span class="n">pprint</span><span class="p">(</span><span class="n">summary</span><span class="p">,</span> <span class="n">compact</span><span class="o">=</span><span class="kc">True</span><span class="p">,</span> <span class="n">sort_dicts</span><span class="o">=</span><span class="kc">False</span><span class="p">)</span>
</span><span id="L-671"><a href="#L-671"><span class="linenos"> 671</span></a>    <span class="k">return</span> <span class="n">summary</span>
</span><span id="L-672"><a href="#L-672"><span class="linenos"> 672</span></a>
</span><span id="L-673"><a href="#L-673"><span class="linenos"> 673</span></a>
</span><span id="L-674"><a href="#L-674"><span class="linenos"> 674</span></a><span class="nd">@typechecked</span>
</span><span id="L-675"><a href="#L-675"><span class="linenos"> 675</span></a><span class="k">def</span> <span class="nf">predict_campaign</span><span class="p">(</span>
</span><span id="L-676"><a href="#L-676"><span class="linenos"> 676</span></a>    <span class="n">filepath_or_df</span><span class="p">:</span> <span class="n">Union</span><span class="p">[</span><span class="nb">str</span><span class="p">,</span> <span class="n">pd</span><span class="o">.</span><span class="n">DataFrame</span><span class="p">],</span>
</span><span id="L-677"><a href="#L-677"><span class="linenos"> 677</span></a>    <span class="n">campaign_id</span><span class="p">:</span> <span class="nb">str</span><span class="p">,</span>
</span><span id="L-678"><a href="#L-678"><span class="linenos"> 678</span></a>    <span class="n">processor</span><span class="p">:</span> <span class="n">Optional</span><span class="p">[</span><span class="nb">str</span><span class="p">]</span> <span class="o">=</span> <span class="s2">&quot;cpu&quot;</span><span class="p">,</span>
</span><span id="L-679"><a href="#L-679"><span class="linenos"> 679</span></a>    <span class="n">verbose</span><span class="p">:</span> <span class="n">Optional</span><span class="p">[</span><span class="nb">bool</span><span class="p">]</span> <span class="o">=</span> <span class="kc">False</span><span class="p">,</span>
</span><span id="L-680"><a href="#L-680"><span class="linenos"> 680</span></a>    <span class="n">debug</span><span class="p">:</span> <span class="n">Optional</span><span class="p">[</span><span class="nb">bool</span><span class="p">]</span> <span class="o">=</span> <span class="kc">False</span><span class="p">,</span>
</span><span id="L-681"><a href="#L-681"><span class="linenos"> 681</span></a><span class="p">)</span> <span class="o">-&gt;</span> <span class="n">Tuple</span><span class="p">[</span><span class="n">pd</span><span class="o">.</span><span class="n">DataFrame</span><span class="p">,</span> <span class="n">pd</span><span class="o">.</span><span class="n">DataFrame</span><span class="p">]:</span>
</span><span id="L-682"><a href="#L-682"><span class="linenos"> 682</span></a><span class="w">    </span><span class="sd">&quot;&quot;&quot;</span>
</span><span id="L-683"><a href="#L-683"><span class="linenos"> 683</span></a><span class="sd">    # Predict campaign</span>
</span><span id="L-684"><a href="#L-684"><span class="linenos"> 684</span></a>
</span><span id="L-685"><a href="#L-685"><span class="linenos"> 685</span></a><span class="sd">    Make predictions from a pre-trained model that exists on the `twinLab` cloud.</span>
</span><span id="L-686"><a href="#L-686"><span class="linenos"> 686</span></a>
</span><span id="L-687"><a href="#L-687"><span class="linenos"> 687</span></a><span class="sd">    ## Arguments</span>
</span><span id="L-688"><a href="#L-688"><span class="linenos"> 688</span></a>
</span><span id="L-689"><a href="#L-689"><span class="linenos"> 689</span></a><span class="sd">    - `filepath_or_df`: `str`; location of csv dataset on local machine for evaluation</span>
</span><span id="L-690"><a href="#L-690"><span class="linenos"> 690</span></a><span class="sd">        or `pandas` dataframe</span>
</span><span id="L-691"><a href="#L-691"><span class="linenos"> 691</span></a><span class="sd">    - `campaign_id`: `str`; name of pre-trained campaign to use for predictions</span>
</span><span id="L-692"><a href="#L-692"><span class="linenos"> 692</span></a><span class="sd">    - `processor`: `str`, Optional, processor to use for sampling (&quot;cpu&quot;; &quot;gpu&quot;)</span>
</span><span id="L-693"><a href="#L-693"><span class="linenos"> 693</span></a><span class="sd">    - `verbose`: `bool`, Optional, determining level of information returned to the user</span>
</span><span id="L-694"><a href="#L-694"><span class="linenos"> 694</span></a><span class="sd">    - `debug`: `bool`, Optional, determining level of information logged on the server</span>
</span><span id="L-695"><a href="#L-695"><span class="linenos"> 695</span></a>
</span><span id="L-696"><a href="#L-696"><span class="linenos"> 696</span></a><span class="sd">    **NOTE:** Evaluation data must be a CSV file, or a `pandas` dataframe that is interpretable as a CSV.</span>
</span><span id="L-697"><a href="#L-697"><span class="linenos"> 697</span></a>
</span><span id="L-698"><a href="#L-698"><span class="linenos"> 698</span></a><span class="sd">    ## Returns</span>
</span><span id="L-699"><a href="#L-699"><span class="linenos"> 699</span></a>
</span><span id="L-700"><a href="#L-700"><span class="linenos"> 700</span></a><span class="sd">    - `tuple` containing:</span>
</span><span id="L-701"><a href="#L-701"><span class="linenos"> 701</span></a><span class="sd">        - `df_mean`: `pandas.DataFrame` containing mean predictions</span>
</span><span id="L-702"><a href="#L-702"><span class="linenos"> 702</span></a><span class="sd">        - `df_std`: `pandas.DataFrame` containing standard deviation predictions</span>
</span><span id="L-703"><a href="#L-703"><span class="linenos"> 703</span></a>
</span><span id="L-704"><a href="#L-704"><span class="linenos"> 704</span></a><span class="sd">    ## Example</span>
</span><span id="L-705"><a href="#L-705"><span class="linenos"> 705</span></a>
</span><span id="L-706"><a href="#L-706"><span class="linenos"> 706</span></a><span class="sd">    Using a local file:</span>
</span><span id="L-707"><a href="#L-707"><span class="linenos"> 707</span></a><span class="sd">    ```python</span>
</span><span id="L-708"><a href="#L-708"><span class="linenos"> 708</span></a><span class="sd">    import pandas as pd</span>
</span><span id="L-709"><a href="#L-709"><span class="linenos"> 709</span></a><span class="sd">    import twinlab as tl</span>
</span><span id="L-710"><a href="#L-710"><span class="linenos"> 710</span></a>
</span><span id="L-711"><a href="#L-711"><span class="linenos"> 711</span></a><span class="sd">    df = pd.DataFrame({&#39;X&#39;: [1, 2, 3, 4], &#39;y&#39;: [1, 4, 9, 16]})</span>
</span><span id="L-712"><a href="#L-712"><span class="linenos"> 712</span></a><span class="sd">    tl.upload_dataset(df, &quot;my_dataset&quot;)</span>
</span><span id="L-713"><a href="#L-713"><span class="linenos"> 713</span></a><span class="sd">    params = {</span>
</span><span id="L-714"><a href="#L-714"><span class="linenos"> 714</span></a><span class="sd">        &quot;dataset_id&quot;: &quot;my_dataset&quot;,</span>
</span><span id="L-715"><a href="#L-715"><span class="linenos"> 715</span></a><span class="sd">        &quot;inputs&quot;: [&quot;X&quot;],</span>
</span><span id="L-716"><a href="#L-716"><span class="linenos"> 716</span></a><span class="sd">        &quot;outputs&quot;: [&quot;y&quot;],</span>
</span><span id="L-717"><a href="#L-717"><span class="linenos"> 717</span></a><span class="sd">    }</span>
</span><span id="L-718"><a href="#L-718"><span class="linenos"> 718</span></a><span class="sd">    tl.train_campaign(params, &quot;my_campaign&quot;)</span>
</span><span id="L-719"><a href="#L-719"><span class="linenos"> 719</span></a><span class="sd">    filepath = &quot;path/to/data.csv&quot; # Local</span>
</span><span id="L-720"><a href="#L-720"><span class="linenos"> 720</span></a><span class="sd">    campaign_id = &#39;my_campaign&quot; # Pre-trained</span>
</span><span id="L-721"><a href="#L-721"><span class="linenos"> 721</span></a><span class="sd">    df_mean, df_std = tl.predict_campaign(filepath, campaign_id)</span>
</span><span id="L-722"><a href="#L-722"><span class="linenos"> 722</span></a><span class="sd">    print(df_mean)</span>
</span><span id="L-723"><a href="#L-723"><span class="linenos"> 723</span></a><span class="sd">    print(df_std)</span>
</span><span id="L-724"><a href="#L-724"><span class="linenos"> 724</span></a><span class="sd">    ```</span>
</span><span id="L-725"><a href="#L-725"><span class="linenos"> 725</span></a>
</span><span id="L-726"><a href="#L-726"><span class="linenos"> 726</span></a><span class="sd">    Using a `pandas` dataframe:</span>
</span><span id="L-727"><a href="#L-727"><span class="linenos"> 727</span></a><span class="sd">    ```python</span>
</span><span id="L-728"><a href="#L-728"><span class="linenos"> 728</span></a><span class="sd">    import pandas as pd</span>
</span><span id="L-729"><a href="#L-729"><span class="linenos"> 729</span></a><span class="sd">    import twinlab as tl</span>
</span><span id="L-730"><a href="#L-730"><span class="linenos"> 730</span></a>
</span><span id="L-731"><a href="#L-731"><span class="linenos"> 731</span></a><span class="sd">    df = pd.DataFrame({&#39;X&#39;: [1, 2, 3, 4], &#39;y&#39;: [1, 4, 9, 16]})</span>
</span><span id="L-732"><a href="#L-732"><span class="linenos"> 732</span></a><span class="sd">    tl.upload_dataset(df, &quot;my_dataset&quot;)</span>
</span><span id="L-733"><a href="#L-733"><span class="linenos"> 733</span></a><span class="sd">    params = {</span>
</span><span id="L-734"><a href="#L-734"><span class="linenos"> 734</span></a><span class="sd">        &quot;dataset_id&quot;: &quot;my_dataset&quot;,</span>
</span><span id="L-735"><a href="#L-735"><span class="linenos"> 735</span></a><span class="sd">        &quot;inputs&quot;: [&quot;X&quot;],</span>
</span><span id="L-736"><a href="#L-736"><span class="linenos"> 736</span></a><span class="sd">        &quot;outputs&quot;: [&quot;y&quot;],</span>
</span><span id="L-737"><a href="#L-737"><span class="linenos"> 737</span></a><span class="sd">    }</span>
</span><span id="L-738"><a href="#L-738"><span class="linenos"> 738</span></a><span class="sd">    tl.train_campaign(params, &quot;my_campaign&quot;)</span>
</span><span id="L-739"><a href="#L-739"><span class="linenos"> 739</span></a><span class="sd">    df = pd.DataFrame({&#39;X&#39;: [1.5, 2.5, 3.5]})</span>
</span><span id="L-740"><a href="#L-740"><span class="linenos"> 740</span></a><span class="sd">    tl.predict_campaign(df, &quot;my_campaign&quot;)</span>
</span><span id="L-741"><a href="#L-741"><span class="linenos"> 741</span></a><span class="sd">    ```</span>
</span><span id="L-742"><a href="#L-742"><span class="linenos"> 742</span></a><span class="sd">    &quot;&quot;&quot;</span>
</span><span id="L-743"><a href="#L-743"><span class="linenos"> 743</span></a>
</span><span id="L-744"><a href="#L-744"><span class="linenos"> 744</span></a>    <span class="n">csv</span> <span class="o">=</span> <span class="n">_use_campaign</span><span class="p">(</span>
</span><span id="L-745"><a href="#L-745"><span class="linenos"> 745</span></a>        <span class="n">campaign_id</span><span class="p">,</span>
</span><span id="L-746"><a href="#L-746"><span class="linenos"> 746</span></a>        <span class="n">method</span><span class="o">=</span><span class="s2">&quot;predict&quot;</span><span class="p">,</span>
</span><span id="L-747"><a href="#L-747"><span class="linenos"> 747</span></a>        <span class="n">filepath_or_df</span><span class="o">=</span><span class="n">filepath_or_df</span><span class="p">,</span>
</span><span id="L-748"><a href="#L-748"><span class="linenos"> 748</span></a>        <span class="n">processor</span><span class="o">=</span><span class="n">processor</span><span class="p">,</span>
</span><span id="L-749"><a href="#L-749"><span class="linenos"> 749</span></a>        <span class="n">verbose</span><span class="o">=</span><span class="n">verbose</span><span class="p">,</span>
</span><span id="L-750"><a href="#L-750"><span class="linenos"> 750</span></a>        <span class="n">debug</span><span class="o">=</span><span class="n">debug</span><span class="p">,</span>
</span><span id="L-751"><a href="#L-751"><span class="linenos"> 751</span></a>    <span class="p">)</span>
</span><span id="L-752"><a href="#L-752"><span class="linenos"> 752</span></a>    <span class="n">df</span> <span class="o">=</span> <span class="n">pd</span><span class="o">.</span><span class="n">read_csv</span><span class="p">(</span><span class="n">csv</span><span class="p">,</span> <span class="n">sep</span><span class="o">=</span><span class="s2">&quot;,&quot;</span><span class="p">)</span>
</span><span id="L-753"><a href="#L-753"><span class="linenos"> 753</span></a>    <span class="n">n</span> <span class="o">=</span> <span class="nb">len</span><span class="p">(</span><span class="n">df</span><span class="o">.</span><span class="n">columns</span><span class="p">)</span>
</span><span id="L-754"><a href="#L-754"><span class="linenos"> 754</span></a>    <span class="n">df_mean</span><span class="p">,</span> <span class="n">df_std</span> <span class="o">=</span> <span class="n">df</span><span class="o">.</span><span class="n">iloc</span><span class="p">[:,</span> <span class="p">:</span> <span class="n">n</span> <span class="o">//</span> <span class="mi">2</span><span class="p">],</span> <span class="n">df</span><span class="o">.</span><span class="n">iloc</span><span class="p">[:,</span> <span class="n">n</span> <span class="o">//</span> <span class="mi">2</span> <span class="p">:]</span>
</span><span id="L-755"><a href="#L-755"><span class="linenos"> 755</span></a>    <span class="n">df_std</span><span class="o">.</span><span class="n">columns</span> <span class="o">=</span> <span class="n">df_std</span><span class="o">.</span><span class="n">columns</span><span class="o">.</span><span class="n">str</span><span class="o">.</span><span class="n">removesuffix</span><span class="p">(</span><span class="s2">&quot; [std_dev]&quot;</span><span class="p">)</span>
</span><span id="L-756"><a href="#L-756"><span class="linenos"> 756</span></a>    <span class="k">if</span> <span class="n">verbose</span><span class="p">:</span>
</span><span id="L-757"><a href="#L-757"><span class="linenos"> 757</span></a>        <span class="nb">print</span><span class="p">(</span><span class="s2">&quot;Mean predictions:&quot;</span><span class="p">)</span>
</span><span id="L-758"><a href="#L-758"><span class="linenos"> 758</span></a>        <span class="nb">print</span><span class="p">(</span><span class="n">df_mean</span><span class="p">)</span>
</span><span id="L-759"><a href="#L-759"><span class="linenos"> 759</span></a>        <span class="nb">print</span><span class="p">(</span><span class="s2">&quot;Standard deviation predictions:&quot;</span><span class="p">)</span>
</span><span id="L-760"><a href="#L-760"><span class="linenos"> 760</span></a>        <span class="nb">print</span><span class="p">(</span><span class="n">df_std</span><span class="p">)</span>
</span><span id="L-761"><a href="#L-761"><span class="linenos"> 761</span></a>
</span><span id="L-762"><a href="#L-762"><span class="linenos"> 762</span></a>    <span class="k">return</span> <span class="n">df_mean</span><span class="p">,</span> <span class="n">df_std</span>
</span><span id="L-763"><a href="#L-763"><span class="linenos"> 763</span></a>
</span><span id="L-764"><a href="#L-764"><span class="linenos"> 764</span></a>
</span><span id="L-765"><a href="#L-765"><span class="linenos"> 765</span></a><span class="nd">@typechecked</span>
</span><span id="L-766"><a href="#L-766"><span class="linenos"> 766</span></a><span class="k">def</span> <span class="nf">sample_campaign</span><span class="p">(</span>
</span><span id="L-767"><a href="#L-767"><span class="linenos"> 767</span></a>    <span class="n">filepath_or_df</span><span class="p">:</span> <span class="n">Union</span><span class="p">[</span><span class="nb">str</span><span class="p">,</span> <span class="n">pd</span><span class="o">.</span><span class="n">DataFrame</span><span class="p">],</span>
</span><span id="L-768"><a href="#L-768"><span class="linenos"> 768</span></a>    <span class="n">campaign_id</span><span class="p">:</span> <span class="nb">str</span><span class="p">,</span>
</span><span id="L-769"><a href="#L-769"><span class="linenos"> 769</span></a>    <span class="n">num_samples</span><span class="p">:</span> <span class="nb">int</span><span class="p">,</span>
</span><span id="L-770"><a href="#L-770"><span class="linenos"> 770</span></a>    <span class="n">processor</span><span class="p">:</span> <span class="n">Optional</span><span class="p">[</span><span class="nb">str</span><span class="p">]</span> <span class="o">=</span> <span class="s2">&quot;cpu&quot;</span><span class="p">,</span>
</span><span id="L-771"><a href="#L-771"><span class="linenos"> 771</span></a>    <span class="n">verbose</span><span class="p">:</span> <span class="n">Optional</span><span class="p">[</span><span class="nb">bool</span><span class="p">]</span> <span class="o">=</span> <span class="kc">False</span><span class="p">,</span>
</span><span id="L-772"><a href="#L-772"><span class="linenos"> 772</span></a>    <span class="n">debug</span><span class="p">:</span> <span class="n">Optional</span><span class="p">[</span><span class="nb">bool</span><span class="p">]</span> <span class="o">=</span> <span class="kc">False</span><span class="p">,</span>
</span><span id="L-773"><a href="#L-773"><span class="linenos"> 773</span></a>    <span class="o">**</span><span class="n">kwargs</span><span class="p">,</span>
</span><span id="L-774"><a href="#L-774"><span class="linenos"> 774</span></a><span class="p">)</span> <span class="o">-&gt;</span> <span class="n">pd</span><span class="o">.</span><span class="n">DataFrame</span><span class="p">:</span>
</span><span id="L-775"><a href="#L-775"><span class="linenos"> 775</span></a><span class="w">    </span><span class="sd">&quot;&quot;&quot;</span>
</span><span id="L-776"><a href="#L-776"><span class="linenos"> 776</span></a><span class="sd">    # Sample campaign</span>
</span><span id="L-777"><a href="#L-777"><span class="linenos"> 777</span></a>
</span><span id="L-778"><a href="#L-778"><span class="linenos"> 778</span></a><span class="sd">    Draw samples from a pre-trained campaign that exists on the `twinLab` cloud.</span>
</span><span id="L-779"><a href="#L-779"><span class="linenos"> 779</span></a>
</span><span id="L-780"><a href="#L-780"><span class="linenos"> 780</span></a><span class="sd">    ## Arguments</span>
</span><span id="L-781"><a href="#L-781"><span class="linenos"> 781</span></a>
</span><span id="L-782"><a href="#L-782"><span class="linenos"> 782</span></a><span class="sd">    - `filepath_or_df`: `str`; location of csv dataset on local machine for evaluation</span>
</span><span id="L-783"><a href="#L-783"><span class="linenos"> 783</span></a><span class="sd">        or `pandas` dataframe</span>
</span><span id="L-784"><a href="#L-784"><span class="linenos"> 784</span></a><span class="sd">    - `campaign_id`: `str`; name of pre-trained campaign to use for predictions</span>
</span><span id="L-785"><a href="#L-785"><span class="linenos"> 785</span></a><span class="sd">    - `num_samples`: `int`; number of samples to draw for each row of the evaluation data</span>
</span><span id="L-786"><a href="#L-786"><span class="linenos"> 786</span></a><span class="sd">    - `processor`: `str`, Optional, processor to use for sampling (&quot;cpu&quot;; &quot;gpu&quot;)</span>
</span><span id="L-787"><a href="#L-787"><span class="linenos"> 787</span></a><span class="sd">    - `verbose`: `bool`, Optional, determining level of information returned to the user</span>
</span><span id="L-788"><a href="#L-788"><span class="linenos"> 788</span></a><span class="sd">    - `debug`: `bool`, Optional, determining level of information logged on the server</span>
</span><span id="L-789"><a href="#L-789"><span class="linenos"> 789</span></a>
</span><span id="L-790"><a href="#L-790"><span class="linenos"> 790</span></a><span class="sd">    **NOTE:** Evaluation data must be a CSV file, or a `pandas` dataframe that is interpretable as a CSV.</span>
</span><span id="L-791"><a href="#L-791"><span class="linenos"> 791</span></a>
</span><span id="L-792"><a href="#L-792"><span class="linenos"> 792</span></a><span class="sd">    ## Returns</span>
</span><span id="L-793"><a href="#L-793"><span class="linenos"> 793</span></a>
</span><span id="L-794"><a href="#L-794"><span class="linenos"> 794</span></a><span class="sd">    - `DataFrame` with the sampled values</span>
</span><span id="L-795"><a href="#L-795"><span class="linenos"> 795</span></a>
</span><span id="L-796"><a href="#L-796"><span class="linenos"> 796</span></a><span class="sd">    ## Example</span>
</span><span id="L-797"><a href="#L-797"><span class="linenos"> 797</span></a>
</span><span id="L-798"><a href="#L-798"><span class="linenos"> 798</span></a><span class="sd">    Using a local file:</span>
</span><span id="L-799"><a href="#L-799"><span class="linenos"> 799</span></a><span class="sd">    ```python</span>
</span><span id="L-800"><a href="#L-800"><span class="linenos"> 800</span></a><span class="sd">    import pandas as pd</span>
</span><span id="L-801"><a href="#L-801"><span class="linenos"> 801</span></a><span class="sd">    import twinlab as tl</span>
</span><span id="L-802"><a href="#L-802"><span class="linenos"> 802</span></a>
</span><span id="L-803"><a href="#L-803"><span class="linenos"> 803</span></a><span class="sd">    df = pd.DataFrame({&#39;X&#39;: [1, 2, 3, 4], &#39;y&#39;: [1, 4, 9, 16]})</span>
</span><span id="L-804"><a href="#L-804"><span class="linenos"> 804</span></a><span class="sd">    tl.upload_dataset(df, &quot;my_dataset&quot;)</span>
</span><span id="L-805"><a href="#L-805"><span class="linenos"> 805</span></a><span class="sd">    params = {</span>
</span><span id="L-806"><a href="#L-806"><span class="linenos"> 806</span></a><span class="sd">        &quot;dataset_id&quot;: &quot;my_dataset&quot;,</span>
</span><span id="L-807"><a href="#L-807"><span class="linenos"> 807</span></a><span class="sd">        &quot;inputs&quot;: [&quot;X&quot;],</span>
</span><span id="L-808"><a href="#L-808"><span class="linenos"> 808</span></a><span class="sd">        &quot;outputs&quot;: [&quot;y&quot;],</span>
</span><span id="L-809"><a href="#L-809"><span class="linenos"> 809</span></a><span class="sd">    }</span>
</span><span id="L-810"><a href="#L-810"><span class="linenos"> 810</span></a><span class="sd">    tl.train_campaign(params, &quot;my_campaign&quot;)</span>
</span><span id="L-811"><a href="#L-811"><span class="linenos"> 811</span></a><span class="sd">    filepath = &quot;path/to/data.csv&quot; # Local</span>
</span><span id="L-812"><a href="#L-812"><span class="linenos"> 812</span></a><span class="sd">    n = 10</span>
</span><span id="L-813"><a href="#L-813"><span class="linenos"> 813</span></a><span class="sd">    df_mean, df_std = tl.sample_campaign(filepath, &quot;my_campaign&quot;, n)</span>
</span><span id="L-814"><a href="#L-814"><span class="linenos"> 814</span></a><span class="sd">    print(df_mean)</span>
</span><span id="L-815"><a href="#L-815"><span class="linenos"> 815</span></a><span class="sd">    print(df_std)</span>
</span><span id="L-816"><a href="#L-816"><span class="linenos"> 816</span></a><span class="sd">    ```</span>
</span><span id="L-817"><a href="#L-817"><span class="linenos"> 817</span></a>
</span><span id="L-818"><a href="#L-818"><span class="linenos"> 818</span></a><span class="sd">    Using a `pandas` dataframe:</span>
</span><span id="L-819"><a href="#L-819"><span class="linenos"> 819</span></a><span class="sd">    ```python</span>
</span><span id="L-820"><a href="#L-820"><span class="linenos"> 820</span></a><span class="sd">    import pandas as pd</span>
</span><span id="L-821"><a href="#L-821"><span class="linenos"> 821</span></a><span class="sd">    import twinlab as tl</span>
</span><span id="L-822"><a href="#L-822"><span class="linenos"> 822</span></a>
</span><span id="L-823"><a href="#L-823"><span class="linenos"> 823</span></a><span class="sd">    df = pd.DataFrame({&#39;X&#39;: [1, 2, 3, 4], &#39;y&#39;: [1, 4, 9, 16]})</span>
</span><span id="L-824"><a href="#L-824"><span class="linenos"> 824</span></a><span class="sd">    tl.upload_dataset(df, &quot;my_dataset&quot;)</span>
</span><span id="L-825"><a href="#L-825"><span class="linenos"> 825</span></a><span class="sd">    params = {</span>
</span><span id="L-826"><a href="#L-826"><span class="linenos"> 826</span></a><span class="sd">        &quot;dataset_id&quot;: &quot;my_dataset&quot;,</span>
</span><span id="L-827"><a href="#L-827"><span class="linenos"> 827</span></a><span class="sd">        &quot;inputs&quot;: [&quot;X&quot;],</span>
</span><span id="L-828"><a href="#L-828"><span class="linenos"> 828</span></a><span class="sd">        &quot;outputs&quot;: [&quot;y&quot;],</span>
</span><span id="L-829"><a href="#L-829"><span class="linenos"> 829</span></a><span class="sd">    }</span>
</span><span id="L-830"><a href="#L-830"><span class="linenos"> 830</span></a><span class="sd">    tl.train_campaign(params, &quot;my_campaign&quot;)</span>
</span><span id="L-831"><a href="#L-831"><span class="linenos"> 831</span></a><span class="sd">    df = pd.DataFrame({&#39;X&#39;: [1.5, 2.5, 3.5]})</span>
</span><span id="L-832"><a href="#L-832"><span class="linenos"> 832</span></a><span class="sd">    n = 10</span>
</span><span id="L-833"><a href="#L-833"><span class="linenos"> 833</span></a><span class="sd">    tl.sample_campaign(df, &quot;my_campaign&quot;, n)</span>
</span><span id="L-834"><a href="#L-834"><span class="linenos"> 834</span></a><span class="sd">    ```</span>
</span><span id="L-835"><a href="#L-835"><span class="linenos"> 835</span></a><span class="sd">    &quot;&quot;&quot;</span>
</span><span id="L-836"><a href="#L-836"><span class="linenos"> 836</span></a>
</span><span id="L-837"><a href="#L-837"><span class="linenos"> 837</span></a>    <span class="n">csv</span> <span class="o">=</span> <span class="n">_use_campaign</span><span class="p">(</span>
</span><span id="L-838"><a href="#L-838"><span class="linenos"> 838</span></a>        <span class="n">campaign_id</span><span class="p">,</span>
</span><span id="L-839"><a href="#L-839"><span class="linenos"> 839</span></a>        <span class="n">method</span><span class="o">=</span><span class="s2">&quot;sample&quot;</span><span class="p">,</span>
</span><span id="L-840"><a href="#L-840"><span class="linenos"> 840</span></a>        <span class="n">filepath_or_df</span><span class="o">=</span><span class="n">filepath_or_df</span><span class="p">,</span>
</span><span id="L-841"><a href="#L-841"><span class="linenos"> 841</span></a>        <span class="n">num_samples</span><span class="o">=</span><span class="n">num_samples</span><span class="p">,</span>
</span><span id="L-842"><a href="#L-842"><span class="linenos"> 842</span></a>        <span class="n">processor</span><span class="o">=</span><span class="n">processor</span><span class="p">,</span>
</span><span id="L-843"><a href="#L-843"><span class="linenos"> 843</span></a>        <span class="n">verbose</span><span class="o">=</span><span class="n">verbose</span><span class="p">,</span>
</span><span id="L-844"><a href="#L-844"><span class="linenos"> 844</span></a>        <span class="n">debug</span><span class="o">=</span><span class="n">debug</span><span class="p">,</span>
</span><span id="L-845"><a href="#L-845"><span class="linenos"> 845</span></a>        <span class="o">**</span><span class="n">kwargs</span><span class="p">,</span>
</span><span id="L-846"><a href="#L-846"><span class="linenos"> 846</span></a>    <span class="p">)</span>
</span><span id="L-847"><a href="#L-847"><span class="linenos"> 847</span></a>    <span class="n">df</span> <span class="o">=</span> <span class="n">pd</span><span class="o">.</span><span class="n">read_csv</span><span class="p">(</span><span class="n">csv</span><span class="p">,</span> <span class="n">header</span><span class="o">=</span><span class="p">[</span><span class="mi">0</span><span class="p">,</span> <span class="mi">1</span><span class="p">],</span> <span class="n">sep</span><span class="o">=</span><span class="s2">&quot;,&quot;</span><span class="p">)</span>
</span><span id="L-848"><a href="#L-848"><span class="linenos"> 848</span></a>    <span class="k">if</span> <span class="n">verbose</span><span class="p">:</span>
</span><span id="L-849"><a href="#L-849"><span class="linenos"> 849</span></a>        <span class="nb">print</span><span class="p">(</span><span class="s2">&quot;Samples:&quot;</span><span class="p">)</span>
</span><span id="L-850"><a href="#L-850"><span class="linenos"> 850</span></a>        <span class="nb">print</span><span class="p">(</span><span class="n">df</span><span class="p">)</span>
</span><span id="L-851"><a href="#L-851"><span class="linenos"> 851</span></a>    <span class="k">return</span> <span class="n">df</span>
</span><span id="L-852"><a href="#L-852"><span class="linenos"> 852</span></a>
</span><span id="L-853"><a href="#L-853"><span class="linenos"> 853</span></a>
</span><span id="L-854"><a href="#L-854"><span class="linenos"> 854</span></a><span class="nd">@typechecked</span>
</span><span id="L-855"><a href="#L-855"><span class="linenos"> 855</span></a><span class="k">def</span> <span class="nf">active_learn_campaign</span><span class="p">(</span>
</span><span id="L-856"><a href="#L-856"><span class="linenos"> 856</span></a>    <span class="n">campaign_id</span><span class="p">:</span> <span class="nb">str</span><span class="p">,</span>
</span><span id="L-857"><a href="#L-857"><span class="linenos"> 857</span></a>    <span class="n">num_points</span><span class="p">:</span> <span class="nb">int</span><span class="p">,</span>
</span><span id="L-858"><a href="#L-858"><span class="linenos"> 858</span></a>    <span class="n">processor</span><span class="p">:</span> <span class="n">Optional</span><span class="p">[</span><span class="nb">str</span><span class="p">]</span> <span class="o">=</span> <span class="s2">&quot;cpu&quot;</span><span class="p">,</span>
</span><span id="L-859"><a href="#L-859"><span class="linenos"> 859</span></a>    <span class="n">verbose</span><span class="p">:</span> <span class="n">Optional</span><span class="p">[</span><span class="nb">bool</span><span class="p">]</span> <span class="o">=</span> <span class="kc">False</span><span class="p">,</span>
</span><span id="L-860"><a href="#L-860"><span class="linenos"> 860</span></a>    <span class="n">debug</span><span class="p">:</span> <span class="n">Optional</span><span class="p">[</span><span class="nb">bool</span><span class="p">]</span> <span class="o">=</span> <span class="kc">False</span><span class="p">,</span>
</span><span id="L-861"><a href="#L-861"><span class="linenos"> 861</span></a>    <span class="o">**</span><span class="n">kwargs</span><span class="p">,</span>
</span><span id="L-862"><a href="#L-862"><span class="linenos"> 862</span></a><span class="p">)</span> <span class="o">-&gt;</span> <span class="n">pd</span><span class="o">.</span><span class="n">DataFrame</span><span class="p">:</span>
</span><span id="L-863"><a href="#L-863"><span class="linenos"> 863</span></a><span class="w">    </span><span class="sd">&quot;&quot;&quot;</span>
</span><span id="L-864"><a href="#L-864"><span class="linenos"> 864</span></a><span class="sd">    # Active learn campaign</span>
</span><span id="L-865"><a href="#L-865"><span class="linenos"> 865</span></a>
</span><span id="L-866"><a href="#L-866"><span class="linenos"> 866</span></a><span class="sd">    Draw new candidate data points via active learning from a pre-trained campaign</span>
</span><span id="L-867"><a href="#L-867"><span class="linenos"> 867</span></a><span class="sd">    that exists on the `twinLab` cloud.</span>
</span><span id="L-868"><a href="#L-868"><span class="linenos"> 868</span></a>
</span><span id="L-869"><a href="#L-869"><span class="linenos"> 869</span></a><span class="sd">    ## Arguments</span>
</span><span id="L-870"><a href="#L-870"><span class="linenos"> 870</span></a><span class="sd">    - `campaign_id`: `str`; name of pre-trained campaign to use for predictions</span>
</span><span id="L-871"><a href="#L-871"><span class="linenos"> 871</span></a><span class="sd">    - `num_points`: `int`; number of samples to draw for each row of the evaluation data</span>
</span><span id="L-872"><a href="#L-872"><span class="linenos"> 872</span></a><span class="sd">    - `processor`: `str`, Optional, processor to use for sampling (&quot;cpu&quot;; &quot;gpu&quot;)</span>
</span><span id="L-873"><a href="#L-873"><span class="linenos"> 873</span></a><span class="sd">    - `verbose`: `bool`, Optional, determining level of information returned to the user</span>
</span><span id="L-874"><a href="#L-874"><span class="linenos"> 874</span></a><span class="sd">    - `debug`: `bool`, Optional, determining level of information logged on the server</span>
</span><span id="L-875"><a href="#L-875"><span class="linenos"> 875</span></a>
</span><span id="L-876"><a href="#L-876"><span class="linenos"> 876</span></a><span class="sd">    ## Returns</span>
</span><span id="L-877"><a href="#L-877"><span class="linenos"> 877</span></a>
</span><span id="L-878"><a href="#L-878"><span class="linenos"> 878</span></a><span class="sd">    - `Dataframe` containing the recommended sample locations</span>
</span><span id="L-879"><a href="#L-879"><span class="linenos"> 879</span></a>
</span><span id="L-880"><a href="#L-880"><span class="linenos"> 880</span></a><span class="sd">    ## Example</span>
</span><span id="L-881"><a href="#L-881"><span class="linenos"> 881</span></a>
</span><span id="L-882"><a href="#L-882"><span class="linenos"> 882</span></a><span class="sd">    ```python</span>
</span><span id="L-883"><a href="#L-883"><span class="linenos"> 883</span></a><span class="sd">    import pandas as pd</span>
</span><span id="L-884"><a href="#L-884"><span class="linenos"> 884</span></a><span class="sd">    import twinlab as tl</span>
</span><span id="L-885"><a href="#L-885"><span class="linenos"> 885</span></a>
</span><span id="L-886"><a href="#L-886"><span class="linenos"> 886</span></a><span class="sd">    df = pd.DataFrame({&#39;X&#39;: [1, 2, 3, 4], &#39;y&#39;: [1, 4, 9, 16]})</span>
</span><span id="L-887"><a href="#L-887"><span class="linenos"> 887</span></a><span class="sd">    tl.upload_dataset(df, &quot;my_dataset&quot;)</span>
</span><span id="L-888"><a href="#L-888"><span class="linenos"> 888</span></a><span class="sd">    params = {</span>
</span><span id="L-889"><a href="#L-889"><span class="linenos"> 889</span></a><span class="sd">        &quot;dataset_id&quot;: &quot;my_dataset&quot;,</span>
</span><span id="L-890"><a href="#L-890"><span class="linenos"> 890</span></a><span class="sd">        &quot;inputs&quot;: [&quot;X&quot;],</span>
</span><span id="L-891"><a href="#L-891"><span class="linenos"> 891</span></a><span class="sd">        &quot;outputs&quot;: [&quot;y&quot;],</span>
</span><span id="L-892"><a href="#L-892"><span class="linenos"> 892</span></a><span class="sd">    }</span>
</span><span id="L-893"><a href="#L-893"><span class="linenos"> 893</span></a><span class="sd">    tl.train_campaign(params, &quot;my_campaign&quot;)</span>
</span><span id="L-894"><a href="#L-894"><span class="linenos"> 894</span></a><span class="sd">    n = 10</span>
</span><span id="L-895"><a href="#L-895"><span class="linenos"> 895</span></a><span class="sd">    df = tl.active_learn_campaign(&quot;my_campaign&quot;, n)</span>
</span><span id="L-896"><a href="#L-896"><span class="linenos"> 896</span></a><span class="sd">    print(df)</span>
</span><span id="L-897"><a href="#L-897"><span class="linenos"> 897</span></a><span class="sd">    ```</span>
</span><span id="L-898"><a href="#L-898"><span class="linenos"> 898</span></a><span class="sd">    &quot;&quot;&quot;</span>
</span><span id="L-899"><a href="#L-899"><span class="linenos"> 899</span></a>
</span><span id="L-900"><a href="#L-900"><span class="linenos"> 900</span></a>    <span class="n">csv</span> <span class="o">=</span> <span class="n">_use_campaign</span><span class="p">(</span>
</span><span id="L-901"><a href="#L-901"><span class="linenos"> 901</span></a>        <span class="n">campaign_id</span><span class="p">,</span>
</span><span id="L-902"><a href="#L-902"><span class="linenos"> 902</span></a>        <span class="n">method</span><span class="o">=</span><span class="s2">&quot;get_candidate_points&quot;</span><span class="p">,</span>
</span><span id="L-903"><a href="#L-903"><span class="linenos"> 903</span></a>        <span class="n">acq_func</span><span class="o">=</span><span class="s2">&quot;qNIPV&quot;</span><span class="p">,</span>
</span><span id="L-904"><a href="#L-904"><span class="linenos"> 904</span></a>        <span class="n">num_points</span><span class="o">=</span><span class="n">num_points</span><span class="p">,</span>
</span><span id="L-905"><a href="#L-905"><span class="linenos"> 905</span></a>        <span class="n">processor</span><span class="o">=</span><span class="n">processor</span><span class="p">,</span>
</span><span id="L-906"><a href="#L-906"><span class="linenos"> 906</span></a>        <span class="n">verbose</span><span class="o">=</span><span class="n">verbose</span><span class="p">,</span>
</span><span id="L-907"><a href="#L-907"><span class="linenos"> 907</span></a>        <span class="n">debug</span><span class="o">=</span><span class="n">debug</span><span class="p">,</span>
</span><span id="L-908"><a href="#L-908"><span class="linenos"> 908</span></a>        <span class="o">**</span><span class="n">kwargs</span><span class="p">,</span>
</span><span id="L-909"><a href="#L-909"><span class="linenos"> 909</span></a>    <span class="p">)</span>
</span><span id="L-910"><a href="#L-910"><span class="linenos"> 910</span></a>    <span class="n">df</span> <span class="o">=</span> <span class="n">pd</span><span class="o">.</span><span class="n">read_csv</span><span class="p">(</span><span class="n">csv</span><span class="p">,</span> <span class="n">sep</span><span class="o">=</span><span class="s2">&quot;,&quot;</span><span class="p">)</span>
</span><span id="L-911"><a href="#L-911"><span class="linenos"> 911</span></a>    <span class="k">if</span> <span class="n">verbose</span><span class="p">:</span>
</span><span id="L-912"><a href="#L-912"><span class="linenos"> 912</span></a>        <span class="nb">print</span><span class="p">(</span><span class="s2">&quot;Candidate points:&quot;</span><span class="p">)</span>
</span><span id="L-913"><a href="#L-913"><span class="linenos"> 913</span></a>        <span class="nb">print</span><span class="p">(</span><span class="n">df</span><span class="p">)</span>
</span><span id="L-914"><a href="#L-914"><span class="linenos"> 914</span></a>    <span class="k">return</span> <span class="n">df</span>
</span><span id="L-915"><a href="#L-915"><span class="linenos"> 915</span></a>
</span><span id="L-916"><a href="#L-916"><span class="linenos"> 916</span></a>
</span><span id="L-917"><a href="#L-917"><span class="linenos"> 917</span></a><span class="nd">@typechecked</span>
</span><span id="L-918"><a href="#L-918"><span class="linenos"> 918</span></a><span class="k">def</span> <span class="nf">optimise_campaign</span><span class="p">(</span>
</span><span id="L-919"><a href="#L-919"><span class="linenos"> 919</span></a>    <span class="n">campaign_id</span><span class="p">:</span> <span class="nb">str</span><span class="p">,</span>
</span><span id="L-920"><a href="#L-920"><span class="linenos"> 920</span></a>    <span class="n">num_points</span><span class="p">:</span> <span class="nb">int</span><span class="p">,</span>
</span><span id="L-921"><a href="#L-921"><span class="linenos"> 921</span></a>    <span class="n">processor</span><span class="p">:</span> <span class="n">Optional</span><span class="p">[</span><span class="nb">str</span><span class="p">]</span> <span class="o">=</span> <span class="s2">&quot;cpu&quot;</span><span class="p">,</span>
</span><span id="L-922"><a href="#L-922"><span class="linenos"> 922</span></a>    <span class="n">verbose</span><span class="p">:</span> <span class="n">Optional</span><span class="p">[</span><span class="nb">bool</span><span class="p">]</span> <span class="o">=</span> <span class="kc">False</span><span class="p">,</span>
</span><span id="L-923"><a href="#L-923"><span class="linenos"> 923</span></a>    <span class="n">debug</span><span class="p">:</span> <span class="n">Optional</span><span class="p">[</span><span class="nb">bool</span><span class="p">]</span> <span class="o">=</span> <span class="kc">False</span><span class="p">,</span>
</span><span id="L-924"><a href="#L-924"><span class="linenos"> 924</span></a>    <span class="o">**</span><span class="n">kwargs</span><span class="p">,</span>
</span><span id="L-925"><a href="#L-925"><span class="linenos"> 925</span></a><span class="p">)</span> <span class="o">-&gt;</span> <span class="n">pd</span><span class="o">.</span><span class="n">DataFrame</span><span class="p">:</span>
</span><span id="L-926"><a href="#L-926"><span class="linenos"> 926</span></a><span class="w">    </span><span class="sd">&quot;&quot;&quot;</span>
</span><span id="L-927"><a href="#L-927"><span class="linenos"> 927</span></a><span class="sd">    # Optimise campaign</span>
</span><span id="L-928"><a href="#L-928"><span class="linenos"> 928</span></a>
</span><span id="L-929"><a href="#L-929"><span class="linenos"> 929</span></a><span class="sd">    Draw new candidate data points by optimizing for &quot;qEI&quot; (Monte Carlo Expected Improvement)</span>
</span><span id="L-930"><a href="#L-930"><span class="linenos"> 930</span></a><span class="sd">    acquisition function from a pre-trained campaign that exists on the `twinLab` cloud.</span>
</span><span id="L-931"><a href="#L-931"><span class="linenos"> 931</span></a>
</span><span id="L-932"><a href="#L-932"><span class="linenos"> 932</span></a><span class="sd">    ## Arguments</span>
</span><span id="L-933"><a href="#L-933"><span class="linenos"> 933</span></a><span class="sd">    - `campaign_id`: `str`, name of pre-trained campaign to use for predictions</span>
</span><span id="L-934"><a href="#L-934"><span class="linenos"> 934</span></a><span class="sd">    - `num_points`: `int`, number of samples to draw for each row of the evaluation data</span>
</span><span id="L-935"><a href="#L-935"><span class="linenos"> 935</span></a><span class="sd">    - `processor`: `str`, Optional, processor to use for sampling (&quot;cpu&quot;; &quot;gpu&quot;)</span>
</span><span id="L-936"><a href="#L-936"><span class="linenos"> 936</span></a><span class="sd">    - `verbose`: `bool`, Optional, determining level of information returned to the user</span>
</span><span id="L-937"><a href="#L-937"><span class="linenos"> 937</span></a><span class="sd">    - `debug`: `bool`, Optional, determining level of information logged on the server</span>
</span><span id="L-938"><a href="#L-938"><span class="linenos"> 938</span></a><span class="sd">    - `acq_kwargs`: `dict`, Optional, specifies the keyword arguments to modify the behavior of</span>
</span><span id="L-939"><a href="#L-939"><span class="linenos"> 939</span></a><span class="sd">        the acquisition function. This dictionary currently allows only one keyword argument</span>
</span><span id="L-940"><a href="#L-940"><span class="linenos"> 940</span></a><span class="sd">        - `weights`: `list[float]`, specifies the weightage for different objectives to be</span>
</span><span id="L-941"><a href="#L-941"><span class="linenos"> 941</span></a><span class="sd">            optimised in a mulit-objective optimisation scenario. By default all weights are equal.</span>
</span><span id="L-942"><a href="#L-942"><span class="linenos"> 942</span></a><span class="sd">            e.g for a problem with 2 outputs if weights are as follows [1, 0.5], this indicates</span>
</span><span id="L-943"><a href="#L-943"><span class="linenos"> 943</span></a><span class="sd">            that we focus on maximising the first output dimension twice as much as</span>
</span><span id="L-944"><a href="#L-944"><span class="linenos"> 944</span></a><span class="sd">            the second output dimension.</span>
</span><span id="L-945"><a href="#L-945"><span class="linenos"> 945</span></a>
</span><span id="L-946"><a href="#L-946"><span class="linenos"> 946</span></a><span class="sd">    ## Returns</span>
</span><span id="L-947"><a href="#L-947"><span class="linenos"> 947</span></a>
</span><span id="L-948"><a href="#L-948"><span class="linenos"> 948</span></a><span class="sd">    - `Dataframe` containing the recommended sample locations</span>
</span><span id="L-949"><a href="#L-949"><span class="linenos"> 949</span></a>
</span><span id="L-950"><a href="#L-950"><span class="linenos"> 950</span></a><span class="sd">    ## Example</span>
</span><span id="L-951"><a href="#L-951"><span class="linenos"> 951</span></a>
</span><span id="L-952"><a href="#L-952"><span class="linenos"> 952</span></a><span class="sd">    ```python</span>
</span><span id="L-953"><a href="#L-953"><span class="linenos"> 953</span></a><span class="sd">    import pandas as pd</span>
</span><span id="L-954"><a href="#L-954"><span class="linenos"> 954</span></a><span class="sd">    import twinlab as tl</span>
</span><span id="L-955"><a href="#L-955"><span class="linenos"> 955</span></a>
</span><span id="L-956"><a href="#L-956"><span class="linenos"> 956</span></a><span class="sd">    df = pd.DataFrame({&#39;X&#39;: [0.0, 0.25, 0.75, 1.0], &#39;y&#39;: [-1.60856306, -0.27526546, -0.34670215, -1.65062947]})</span>
</span><span id="L-957"><a href="#L-957"><span class="linenos"> 957</span></a><span class="sd">    tl.upload_dataset(df, &quot;my_dataset&quot;)</span>
</span><span id="L-958"><a href="#L-958"><span class="linenos"> 958</span></a><span class="sd">    params = {</span>
</span><span id="L-959"><a href="#L-959"><span class="linenos"> 959</span></a><span class="sd">        &quot;dataset_id&quot;: &quot;my_dataset&quot;,</span>
</span><span id="L-960"><a href="#L-960"><span class="linenos"> 960</span></a><span class="sd">        &quot;inputs&quot;: [&quot;X&quot;],</span>
</span><span id="L-961"><a href="#L-961"><span class="linenos"> 961</span></a><span class="sd">        &quot;outputs&quot;: [&quot;y&quot;],</span>
</span><span id="L-962"><a href="#L-962"><span class="linenos"> 962</span></a><span class="sd">    }</span>
</span><span id="L-963"><a href="#L-963"><span class="linenos"> 963</span></a><span class="sd">    tl.train_campaign(params, &quot;my_campaign&quot;)</span>
</span><span id="L-964"><a href="#L-964"><span class="linenos"> 964</span></a><span class="sd">    n = 1</span>
</span><span id="L-965"><a href="#L-965"><span class="linenos"> 965</span></a><span class="sd">    df = tl.optimise_campaign(&quot;my_campaign&quot;, n)</span>
</span><span id="L-966"><a href="#L-966"><span class="linenos"> 966</span></a><span class="sd">    print(df)</span>
</span><span id="L-967"><a href="#L-967"><span class="linenos"> 967</span></a><span class="sd">    ```</span>
</span><span id="L-968"><a href="#L-968"><span class="linenos"> 968</span></a><span class="sd">    &quot;&quot;&quot;</span>
</span><span id="L-969"><a href="#L-969"><span class="linenos"> 969</span></a>
</span><span id="L-970"><a href="#L-970"><span class="linenos"> 970</span></a>    <span class="n">csv</span> <span class="o">=</span> <span class="n">_use_campaign</span><span class="p">(</span>
</span><span id="L-971"><a href="#L-971"><span class="linenos"> 971</span></a>        <span class="n">campaign_id</span><span class="p">,</span>
</span><span id="L-972"><a href="#L-972"><span class="linenos"> 972</span></a>        <span class="n">method</span><span class="o">=</span><span class="s2">&quot;get_candidate_points&quot;</span><span class="p">,</span>
</span><span id="L-973"><a href="#L-973"><span class="linenos"> 973</span></a>        <span class="n">acq_func</span><span class="o">=</span><span class="s2">&quot;qEI&quot;</span><span class="p">,</span>
</span><span id="L-974"><a href="#L-974"><span class="linenos"> 974</span></a>        <span class="n">num_points</span><span class="o">=</span><span class="n">num_points</span><span class="p">,</span>
</span><span id="L-975"><a href="#L-975"><span class="linenos"> 975</span></a>        <span class="n">processor</span><span class="o">=</span><span class="n">processor</span><span class="p">,</span>
</span><span id="L-976"><a href="#L-976"><span class="linenos"> 976</span></a>        <span class="n">verbose</span><span class="o">=</span><span class="n">verbose</span><span class="p">,</span>
</span><span id="L-977"><a href="#L-977"><span class="linenos"> 977</span></a>        <span class="n">debug</span><span class="o">=</span><span class="n">debug</span><span class="p">,</span>
</span><span id="L-978"><a href="#L-978"><span class="linenos"> 978</span></a>        <span class="o">**</span><span class="n">kwargs</span><span class="p">,</span>
</span><span id="L-979"><a href="#L-979"><span class="linenos"> 979</span></a>    <span class="p">)</span>
</span><span id="L-980"><a href="#L-980"><span class="linenos"> 980</span></a>    <span class="n">df</span> <span class="o">=</span> <span class="n">pd</span><span class="o">.</span><span class="n">read_csv</span><span class="p">(</span><span class="n">csv</span><span class="p">,</span> <span class="n">sep</span><span class="o">=</span><span class="s2">&quot;,&quot;</span><span class="p">)</span>
</span><span id="L-981"><a href="#L-981"><span class="linenos"> 981</span></a>    <span class="k">if</span> <span class="n">verbose</span><span class="p">:</span>
</span><span id="L-982"><a href="#L-982"><span class="linenos"> 982</span></a>        <span class="nb">print</span><span class="p">(</span><span class="s2">&quot;Candidate points:&quot;</span><span class="p">)</span>
</span><span id="L-983"><a href="#L-983"><span class="linenos"> 983</span></a>        <span class="nb">print</span><span class="p">(</span><span class="n">df</span><span class="p">)</span>
</span><span id="L-984"><a href="#L-984"><span class="linenos"> 984</span></a>    <span class="k">return</span> <span class="n">df</span>
</span><span id="L-985"><a href="#L-985"><span class="linenos"> 985</span></a>
</span><span id="L-986"><a href="#L-986"><span class="linenos"> 986</span></a>
</span><span id="L-987"><a href="#L-987"><span class="linenos"> 987</span></a><span class="nd">@typechecked</span>
</span><span id="L-988"><a href="#L-988"><span class="linenos"> 988</span></a><span class="k">def</span> <span class="nf">solve_inverse_campaign</span><span class="p">(</span>
</span><span id="L-989"><a href="#L-989"><span class="linenos"> 989</span></a>    <span class="n">campaign_id</span><span class="p">:</span> <span class="nb">str</span><span class="p">,</span>
</span><span id="L-990"><a href="#L-990"><span class="linenos"> 990</span></a>    <span class="n">filepath_or_df</span><span class="p">:</span> <span class="n">Union</span><span class="p">[</span><span class="nb">str</span><span class="p">,</span> <span class="n">pd</span><span class="o">.</span><span class="n">DataFrame</span><span class="p">],</span>
</span><span id="L-991"><a href="#L-991"><span class="linenos"> 991</span></a>    <span class="n">filepath_or_df_std</span><span class="p">:</span> <span class="n">Union</span><span class="p">[</span><span class="nb">str</span><span class="p">,</span> <span class="n">pd</span><span class="o">.</span><span class="n">DataFrame</span><span class="p">],</span>
</span><span id="L-992"><a href="#L-992"><span class="linenos"> 992</span></a>    <span class="n">processor</span><span class="p">:</span> <span class="n">Optional</span><span class="p">[</span><span class="nb">str</span><span class="p">]</span> <span class="o">=</span> <span class="s2">&quot;cpu&quot;</span><span class="p">,</span>
</span><span id="L-993"><a href="#L-993"><span class="linenos"> 993</span></a>    <span class="n">verbose</span><span class="p">:</span> <span class="n">Optional</span><span class="p">[</span><span class="nb">bool</span><span class="p">]</span> <span class="o">=</span> <span class="kc">False</span><span class="p">,</span>
</span><span id="L-994"><a href="#L-994"><span class="linenos"> 994</span></a>    <span class="n">debug</span><span class="p">:</span> <span class="n">Optional</span><span class="p">[</span><span class="nb">bool</span><span class="p">]</span> <span class="o">=</span> <span class="kc">False</span><span class="p">,</span>
</span><span id="L-995"><a href="#L-995"><span class="linenos"> 995</span></a>    <span class="o">**</span><span class="n">kwargs</span><span class="p">,</span>
</span><span id="L-996"><a href="#L-996"><span class="linenos"> 996</span></a><span class="p">)</span> <span class="o">-&gt;</span> <span class="n">pd</span><span class="o">.</span><span class="n">DataFrame</span><span class="p">:</span>
</span><span id="L-997"><a href="#L-997"><span class="linenos"> 997</span></a><span class="w">    </span><span class="sd">&quot;&quot;&quot;</span>
</span><span id="L-998"><a href="#L-998"><span class="linenos"> 998</span></a><span class="sd">    # Inverse modelling on campaign</span>
</span><span id="L-999"><a href="#L-999"><span class="linenos"> 999</span></a>
</span><span id="L-1000"><a href="#L-1000"><span class="linenos">1000</span></a><span class="sd">    Given a set of observations, inverse modelling finds the model that would best suit the data.</span>
</span><span id="L-1001"><a href="#L-1001"><span class="linenos">1001</span></a>
</span><span id="L-1002"><a href="#L-1002"><span class="linenos">1002</span></a><span class="sd">    ## Arguments</span>
</span><span id="L-1003"><a href="#L-1003"><span class="linenos">1003</span></a><span class="sd">    - `campaign_id`: `str`; name of pre-trained campaign to use for predictions</span>
</span><span id="L-1004"><a href="#L-1004"><span class="linenos">1004</span></a><span class="sd">    - `data_csv`: `DataFrame`; a DataFrame of observations</span>
</span><span id="L-1005"><a href="#L-1005"><span class="linenos">1005</span></a><span class="sd">    - `data_std_csv` : `DataFrame`; a DataFrame of errors on the observations</span>
</span><span id="L-1006"><a href="#L-1006"><span class="linenos">1006</span></a><span class="sd">    - `processor`: `str`; processor to use for sampling (&quot;cpu&quot;; &quot;gpu&quot;)</span>
</span><span id="L-1007"><a href="#L-1007"><span class="linenos">1007</span></a><span class="sd">    - `verbose`: `bool` determining level of information returned to the user</span>
</span><span id="L-1008"><a href="#L-1008"><span class="linenos">1008</span></a><span class="sd">    - `debug`: `bool` determining level of information logged on the server</span>
</span><span id="L-1009"><a href="#L-1009"><span class="linenos">1009</span></a>
</span><span id="L-1010"><a href="#L-1010"><span class="linenos">1010</span></a><span class="sd">    ## Returns</span>
</span><span id="L-1011"><a href="#L-1011"><span class="linenos">1011</span></a>
</span><span id="L-1012"><a href="#L-1012"><span class="linenos">1012</span></a><span class="sd">    - `Dataframe` containing the recommended model statistics</span>
</span><span id="L-1013"><a href="#L-1013"><span class="linenos">1013</span></a>
</span><span id="L-1014"><a href="#L-1014"><span class="linenos">1014</span></a><span class="sd">    ## Example</span>
</span><span id="L-1015"><a href="#L-1015"><span class="linenos">1015</span></a>
</span><span id="L-1016"><a href="#L-1016"><span class="linenos">1016</span></a><span class="sd">    ```python</span>
</span><span id="L-1017"><a href="#L-1017"><span class="linenos">1017</span></a><span class="sd">    import pandas as pd</span>
</span><span id="L-1018"><a href="#L-1018"><span class="linenos">1018</span></a><span class="sd">    import twinlab as tl</span>
</span><span id="L-1019"><a href="#L-1019"><span class="linenos">1019</span></a>
</span><span id="L-1020"><a href="#L-1020"><span class="linenos">1020</span></a><span class="sd">    df = pd.DataFrame({&#39;X&#39;: [1, 2, 3, 4], &#39;y&#39;: [1, 4, 9, 16]})</span>
</span><span id="L-1021"><a href="#L-1021"><span class="linenos">1021</span></a><span class="sd">    tl.upload_dataset(df, &quot;my_dataset&quot;)</span>
</span><span id="L-1022"><a href="#L-1022"><span class="linenos">1022</span></a><span class="sd">    params = {</span>
</span><span id="L-1023"><a href="#L-1023"><span class="linenos">1023</span></a><span class="sd">        &quot;dataset_id&quot;: &quot;my_dataset&quot;,</span>
</span><span id="L-1024"><a href="#L-1024"><span class="linenos">1024</span></a><span class="sd">        &quot;inputs&quot;: [&quot;X&quot;],</span>
</span><span id="L-1025"><a href="#L-1025"><span class="linenos">1025</span></a><span class="sd">        &quot;outputs&quot;: [&quot;y&quot;],</span>
</span><span id="L-1026"><a href="#L-1026"><span class="linenos">1026</span></a><span class="sd">    }</span>
</span><span id="L-1027"><a href="#L-1027"><span class="linenos">1027</span></a><span class="sd">    tl.train_campaign(params, &quot;my_campaign&quot;)</span>
</span><span id="L-1028"><a href="#L-1028"><span class="linenos">1028</span></a><span class="sd">    data_csv = pd.DataFrame({&#39;y&#39;: [1]})</span>
</span><span id="L-1029"><a href="#L-1029"><span class="linenos">1029</span></a><span class="sd">    data_std_csv = pd.DataFrame({&#39;y&#39;: [0.498]})</span>
</span><span id="L-1030"><a href="#L-1030"><span class="linenos">1030</span></a><span class="sd">    df = tl.solve_inverse_campaign(&quot;my_campaign&quot;, data_csv, data_std_csv)</span>
</span><span id="L-1031"><a href="#L-1031"><span class="linenos">1031</span></a><span class="sd">    print(df)</span>
</span><span id="L-1032"><a href="#L-1032"><span class="linenos">1032</span></a><span class="sd">    ```</span>
</span><span id="L-1033"><a href="#L-1033"><span class="linenos">1033</span></a><span class="sd">    &quot;&quot;&quot;</span>
</span><span id="L-1034"><a href="#L-1034"><span class="linenos">1034</span></a>    <span class="n">csv</span> <span class="o">=</span> <span class="n">_use_campaign</span><span class="p">(</span>
</span><span id="L-1035"><a href="#L-1035"><span class="linenos">1035</span></a>        <span class="n">campaign_id</span><span class="p">,</span>
</span><span id="L-1036"><a href="#L-1036"><span class="linenos">1036</span></a>        <span class="n">method</span><span class="o">=</span><span class="s2">&quot;solve_inverse&quot;</span><span class="p">,</span>
</span><span id="L-1037"><a href="#L-1037"><span class="linenos">1037</span></a>        <span class="n">filepath_or_df</span><span class="o">=</span><span class="n">filepath_or_df</span><span class="p">,</span>
</span><span id="L-1038"><a href="#L-1038"><span class="linenos">1038</span></a>        <span class="n">filepath_or_df_std</span><span class="o">=</span><span class="n">filepath_or_df_std</span><span class="p">,</span>
</span><span id="L-1039"><a href="#L-1039"><span class="linenos">1039</span></a>        <span class="n">processor</span><span class="o">=</span><span class="n">processor</span><span class="p">,</span>
</span><span id="L-1040"><a href="#L-1040"><span class="linenos">1040</span></a>        <span class="n">verbose</span><span class="o">=</span><span class="n">verbose</span><span class="p">,</span>
</span><span id="L-1041"><a href="#L-1041"><span class="linenos">1041</span></a>        <span class="n">debug</span><span class="o">=</span><span class="n">debug</span><span class="p">,</span>
</span><span id="L-1042"><a href="#L-1042"><span class="linenos">1042</span></a>        <span class="o">**</span><span class="n">kwargs</span><span class="p">,</span>
</span><span id="L-1043"><a href="#L-1043"><span class="linenos">1043</span></a>    <span class="p">)</span>
</span><span id="L-1044"><a href="#L-1044"><span class="linenos">1044</span></a>
</span><span id="L-1045"><a href="#L-1045"><span class="linenos">1045</span></a>    <span class="n">df</span> <span class="o">=</span> <span class="n">pd</span><span class="o">.</span><span class="n">read_csv</span><span class="p">(</span><span class="n">csv</span><span class="p">,</span> <span class="n">sep</span><span class="o">=</span><span class="s2">&quot;,&quot;</span><span class="p">)</span>
</span><span id="L-1046"><a href="#L-1046"><span class="linenos">1046</span></a>    <span class="k">if</span> <span class="n">verbose</span><span class="p">:</span>
</span><span id="L-1047"><a href="#L-1047"><span class="linenos">1047</span></a>        <span class="nb">print</span><span class="p">(</span><span class="s2">&quot;Inverse model statistics:&quot;</span><span class="p">)</span>
</span><span id="L-1048"><a href="#L-1048"><span class="linenos">1048</span></a>        <span class="nb">print</span><span class="p">(</span><span class="n">df</span><span class="p">)</span>
</span><span id="L-1049"><a href="#L-1049"><span class="linenos">1049</span></a>    <span class="k">return</span> <span class="n">df</span>
</span><span id="L-1050"><a href="#L-1050"><span class="linenos">1050</span></a>
</span><span id="L-1051"><a href="#L-1051"><span class="linenos">1051</span></a>
</span><span id="L-1052"><a href="#L-1052"><span class="linenos">1052</span></a><span class="nd">@typechecked</span>
</span><span id="L-1053"><a href="#L-1053"><span class="linenos">1053</span></a><span class="k">def</span> <span class="nf">delete_campaign</span><span class="p">(</span>
</span><span id="L-1054"><a href="#L-1054"><span class="linenos">1054</span></a>    <span class="n">campaign_id</span><span class="p">:</span> <span class="nb">str</span><span class="p">,</span> <span class="n">verbose</span><span class="p">:</span> <span class="n">Optional</span><span class="p">[</span><span class="nb">bool</span><span class="p">]</span> <span class="o">=</span> <span class="kc">False</span><span class="p">,</span> <span class="n">debug</span><span class="p">:</span> <span class="n">Optional</span><span class="p">[</span><span class="nb">bool</span><span class="p">]</span> <span class="o">=</span> <span class="kc">False</span>
</span><span id="L-1055"><a href="#L-1055"><span class="linenos">1055</span></a><span class="p">)</span> <span class="o">-&gt;</span> <span class="kc">None</span><span class="p">:</span>
</span><span id="L-1056"><a href="#L-1056"><span class="linenos">1056</span></a><span class="w">    </span><span class="sd">&quot;&quot;&quot;</span>
</span><span id="L-1057"><a href="#L-1057"><span class="linenos">1057</span></a><span class="sd">    # Delete campaign</span>
</span><span id="L-1058"><a href="#L-1058"><span class="linenos">1058</span></a>
</span><span id="L-1059"><a href="#L-1059"><span class="linenos">1059</span></a><span class="sd">    Delete campaign from the `twinLab` cloud.</span>
</span><span id="L-1060"><a href="#L-1060"><span class="linenos">1060</span></a>
</span><span id="L-1061"><a href="#L-1061"><span class="linenos">1061</span></a><span class="sd">    ## Arguments</span>
</span><span id="L-1062"><a href="#L-1062"><span class="linenos">1062</span></a>
</span><span id="L-1063"><a href="#L-1063"><span class="linenos">1063</span></a><span class="sd">    - `campaign_id`: `str`; name of trained campaign to delete from the cloud</span>
</span><span id="L-1064"><a href="#L-1064"><span class="linenos">1064</span></a><span class="sd">    - `verbose`: `bool`, Optional, determining level of information returned to the user</span>
</span><span id="L-1065"><a href="#L-1065"><span class="linenos">1065</span></a><span class="sd">    - `debug`: `bool`, Optional, determining level of information logged on the server</span>
</span><span id="L-1066"><a href="#L-1066"><span class="linenos">1066</span></a>
</span><span id="L-1067"><a href="#L-1067"><span class="linenos">1067</span></a><span class="sd">    ## Example</span>
</span><span id="L-1068"><a href="#L-1068"><span class="linenos">1068</span></a>
</span><span id="L-1069"><a href="#L-1069"><span class="linenos">1069</span></a><span class="sd">    ```python</span>
</span><span id="L-1070"><a href="#L-1070"><span class="linenos">1070</span></a><span class="sd">    import pandas as pd</span>
</span><span id="L-1071"><a href="#L-1071"><span class="linenos">1071</span></a><span class="sd">    import twinlab as tl</span>
</span><span id="L-1072"><a href="#L-1072"><span class="linenos">1072</span></a>
</span><span id="L-1073"><a href="#L-1073"><span class="linenos">1073</span></a><span class="sd">    df = pd.DataFrame({&#39;X&#39;: [1, 2, 3, 4], &#39;y&#39;: [1, 4, 9, 16]})</span>
</span><span id="L-1074"><a href="#L-1074"><span class="linenos">1074</span></a><span class="sd">    tl.upload_dataset(df, &quot;my_dataset&quot;)</span>
</span><span id="L-1075"><a href="#L-1075"><span class="linenos">1075</span></a><span class="sd">    params = {</span>
</span><span id="L-1076"><a href="#L-1076"><span class="linenos">1076</span></a><span class="sd">        &quot;dataset_id&quot;: &quot;my_dataset&quot;,</span>
</span><span id="L-1077"><a href="#L-1077"><span class="linenos">1077</span></a><span class="sd">        &quot;inputs&quot;: [&quot;X&quot;],</span>
</span><span id="L-1078"><a href="#L-1078"><span class="linenos">1078</span></a><span class="sd">        &quot;outputs&quot;: [&quot;y&quot;],</span>
</span><span id="L-1079"><a href="#L-1079"><span class="linenos">1079</span></a><span class="sd">    }</span>
</span><span id="L-1080"><a href="#L-1080"><span class="linenos">1080</span></a><span class="sd">    tl.train_campaign(params, &quot;my_campaign&quot;)</span>
</span><span id="L-1081"><a href="#L-1081"><span class="linenos">1081</span></a><span class="sd">    tl.delete_campaign(&quot;my_campaign&quot;)</span>
</span><span id="L-1082"><a href="#L-1082"><span class="linenos">1082</span></a><span class="sd">    ```</span>
</span><span id="L-1083"><a href="#L-1083"><span class="linenos">1083</span></a><span class="sd">    &quot;&quot;&quot;</span>
</span><span id="L-1084"><a href="#L-1084"><span class="linenos">1084</span></a>    <span class="n">response</span> <span class="o">=</span> <span class="n">api</span><span class="o">.</span><span class="n">delete_model</span><span class="p">(</span><span class="n">campaign_id</span><span class="p">,</span> <span class="n">verbose</span><span class="o">=</span><span class="n">debug</span><span class="p">)</span>
</span><span id="L-1085"><a href="#L-1085"><span class="linenos">1085</span></a>    <span class="k">if</span> <span class="n">verbose</span><span class="p">:</span>
</span><span id="L-1086"><a href="#L-1086"><span class="linenos">1086</span></a>        <span class="n">message</span> <span class="o">=</span> <span class="n">_get_message</span><span class="p">(</span><span class="n">response</span><span class="p">)</span>
</span><span id="L-1087"><a href="#L-1087"><span class="linenos">1087</span></a>        <span class="nb">print</span><span class="p">(</span><span class="n">message</span><span class="p">)</span>
</span><span id="L-1088"><a href="#L-1088"><span class="linenos">1088</span></a>
</span><span id="L-1089"><a href="#L-1089"><span class="linenos">1089</span></a>
</span><span id="L-1090"><a href="#L-1090"><span class="linenos">1090</span></a><span class="c1">### ###</span>
</span></pre></div>


            </section>
                <section id="get_value_from_body">
                            <input id="get_value_from_body-view-source" class="view-source-toggle-state" type="checkbox" aria-hidden="true" tabindex="-1">
<div class="attr function">
            
        <span class="def">def</span>
        <span class="name">get_value_from_body</span><span class="signature pdoc-code condensed">(<span class="param"><span class="n">key</span><span class="p">:</span> <span class="nb">str</span>, </span><span class="param"><span class="n">body</span><span class="p">:</span> <span class="nb">dict</span></span><span class="return-annotation">):</span></span>

                <label class="view-source-button" for="get_value_from_body-view-source"><span>View Source</span></label>

    </div>
    <a class="headerlink" href="#get_value_from_body"></a>
            <div class="pdoc-code codehilite"><pre><span></span><span id="get_value_from_body-22"><a href="#get_value_from_body-22"><span class="linenos">22</span></a><span class="k">def</span> <span class="nf">get_value_from_body</span><span class="p">(</span><span class="n">key</span><span class="p">:</span> <span class="nb">str</span><span class="p">,</span> <span class="n">body</span><span class="p">:</span> <span class="nb">dict</span><span class="p">):</span>
</span><span id="get_value_from_body-23"><a href="#get_value_from_body-23"><span class="linenos">23</span></a>    <span class="c1"># Improve the error messaging and relate response from api.py directly here</span>
</span><span id="get_value_from_body-24"><a href="#get_value_from_body-24"><span class="linenos">24</span></a>    <span class="k">if</span> <span class="n">key</span> <span class="ow">in</span> <span class="n">body</span><span class="o">.</span><span class="n">keys</span><span class="p">():</span>
</span><span id="get_value_from_body-25"><a href="#get_value_from_body-25"><span class="linenos">25</span></a>        <span class="k">return</span> <span class="n">body</span><span class="p">[</span><span class="sa">f</span><span class="s2">&quot;</span><span class="si">{</span><span class="n">key</span><span class="si">}</span><span class="s2">&quot;</span><span class="p">]</span>
</span><span id="get_value_from_body-26"><a href="#get_value_from_body-26"><span class="linenos">26</span></a>    <span class="k">else</span><span class="p">:</span>
</span><span id="get_value_from_body-27"><a href="#get_value_from_body-27"><span class="linenos">27</span></a>        <span class="nb">print</span><span class="p">(</span><span class="n">body</span><span class="p">)</span>
</span><span id="get_value_from_body-28"><a href="#get_value_from_body-28"><span class="linenos">28</span></a>        <span class="k">raise</span> <span class="ne">KeyError</span><span class="p">(</span><span class="sa">f</span><span class="s2">&quot;</span><span class="si">{</span><span class="n">key</span><span class="si">}</span><span class="s2"> not in API response body&quot;</span><span class="p">)</span>
</span></pre></div>


    

                </section>
                <section id="get_user_information">
                            <input id="get_user_information-view-source" class="view-source-toggle-state" type="checkbox" aria-hidden="true" tabindex="-1">
<div class="attr function">
            
        <span class="def">def</span>
        <span class="name">get_user_information</span><span class="signature pdoc-code condensed">(<span class="param"><span class="n">verbose</span><span class="p">:</span> <span class="n">Optional</span><span class="p">[</span><span class="nb">bool</span><span class="p">]</span> <span class="o">=</span> <span class="kc">False</span>, </span><span class="param"><span class="n">debug</span><span class="p">:</span> <span class="n">Optional</span><span class="p">[</span><span class="nb">bool</span><span class="p">]</span> <span class="o">=</span> <span class="kc">False</span></span><span class="return-annotation">) -> <span class="nb">dict</span>:</span></span>

                <label class="view-source-button" for="get_user_information-view-source"><span>View Source</span></label>

    </div>
    <a class="headerlink" href="#get_user_information"></a>
            <div class="pdoc-code codehilite"><pre><span></span><span id="get_user_information-103"><a href="#get_user_information-103"><span class="linenos">103</span></a><span class="k">def</span> <span class="nf">get_user_information</span><span class="p">(</span>
</span><span id="get_user_information-104"><a href="#get_user_information-104"><span class="linenos">104</span></a>    <span class="n">verbose</span><span class="p">:</span> <span class="n">Optional</span><span class="p">[</span><span class="nb">bool</span><span class="p">]</span> <span class="o">=</span> <span class="kc">False</span><span class="p">,</span> <span class="n">debug</span><span class="p">:</span> <span class="n">Optional</span><span class="p">[</span><span class="nb">bool</span><span class="p">]</span> <span class="o">=</span> <span class="kc">False</span>
</span><span id="get_user_information-105"><a href="#get_user_information-105"><span class="linenos">105</span></a><span class="p">)</span> <span class="o">-&gt;</span> <span class="nb">dict</span><span class="p">:</span>
</span><span id="get_user_information-106"><a href="#get_user_information-106"><span class="linenos">106</span></a><span class="w">    </span><span class="sd">&quot;&quot;&quot;</span>
</span><span id="get_user_information-107"><a href="#get_user_information-107"><span class="linenos">107</span></a><span class="sd">    # Get user information</span>
</span><span id="get_user_information-108"><a href="#get_user_information-108"><span class="linenos">108</span></a>
</span><span id="get_user_information-109"><a href="#get_user_information-109"><span class="linenos">109</span></a><span class="sd">    Get information about the user</span>
</span><span id="get_user_information-110"><a href="#get_user_information-110"><span class="linenos">110</span></a>
</span><span id="get_user_information-111"><a href="#get_user_information-111"><span class="linenos">111</span></a><span class="sd">    ## Arguments</span>
</span><span id="get_user_information-112"><a href="#get_user_information-112"><span class="linenos">112</span></a>
</span><span id="get_user_information-113"><a href="#get_user_information-113"><span class="linenos">113</span></a><span class="sd">    - `verbose`: `bool`, Optional, determining level of information returned to the user</span>
</span><span id="get_user_information-114"><a href="#get_user_information-114"><span class="linenos">114</span></a><span class="sd">    - `debug`: `bool`, Optional, determining level of information logged on the server</span>
</span><span id="get_user_information-115"><a href="#get_user_information-115"><span class="linenos">115</span></a>
</span><span id="get_user_information-116"><a href="#get_user_information-116"><span class="linenos">116</span></a><span class="sd">    ## Returns</span>
</span><span id="get_user_information-117"><a href="#get_user_information-117"><span class="linenos">117</span></a>
</span><span id="get_user_information-118"><a href="#get_user_information-118"><span class="linenos">118</span></a><span class="sd">    - `dict` containing user information</span>
</span><span id="get_user_information-119"><a href="#get_user_information-119"><span class="linenos">119</span></a>
</span><span id="get_user_information-120"><a href="#get_user_information-120"><span class="linenos">120</span></a><span class="sd">    ## Example</span>
</span><span id="get_user_information-121"><a href="#get_user_information-121"><span class="linenos">121</span></a><span class="sd">    ```python</span>
</span><span id="get_user_information-122"><a href="#get_user_information-122"><span class="linenos">122</span></a><span class="sd">    import twinlab as tl</span>
</span><span id="get_user_information-123"><a href="#get_user_information-123"><span class="linenos">123</span></a>
</span><span id="get_user_information-124"><a href="#get_user_information-124"><span class="linenos">124</span></a><span class="sd">    user_info = tl.get_user_information()</span>
</span><span id="get_user_information-125"><a href="#get_user_information-125"><span class="linenos">125</span></a><span class="sd">    print(user_info)</span>
</span><span id="get_user_information-126"><a href="#get_user_information-126"><span class="linenos">126</span></a><span class="sd">    ```</span>
</span><span id="get_user_information-127"><a href="#get_user_information-127"><span class="linenos">127</span></a><span class="sd">    &quot;&quot;&quot;</span>
</span><span id="get_user_information-128"><a href="#get_user_information-128"><span class="linenos">128</span></a>    <span class="n">response</span> <span class="o">=</span> <span class="n">api</span><span class="o">.</span><span class="n">get_user</span><span class="p">(</span><span class="n">verbose</span><span class="o">=</span><span class="n">debug</span><span class="p">)</span>
</span><span id="get_user_information-129"><a href="#get_user_information-129"><span class="linenos">129</span></a>    <span class="n">user_info</span> <span class="o">=</span> <span class="n">response</span>
</span><span id="get_user_information-130"><a href="#get_user_information-130"><span class="linenos">130</span></a>    <span class="k">if</span> <span class="n">verbose</span><span class="p">:</span>
</span><span id="get_user_information-131"><a href="#get_user_information-131"><span class="linenos">131</span></a>        <span class="nb">print</span><span class="p">(</span><span class="s2">&quot;User information:&quot;</span><span class="p">)</span>
</span><span id="get_user_information-132"><a href="#get_user_information-132"><span class="linenos">132</span></a>        <span class="n">pprint</span><span class="p">(</span><span class="n">user_info</span><span class="p">,</span> <span class="n">compact</span><span class="o">=</span><span class="kc">True</span><span class="p">,</span> <span class="n">sort_dicts</span><span class="o">=</span><span class="kc">False</span><span class="p">)</span>
</span><span id="get_user_information-133"><a href="#get_user_information-133"><span class="linenos">133</span></a>    <span class="k">return</span> <span class="n">user_info</span>
</span></pre></div>


            <div class="docstring"><h1 id="get-user-information">Get user information</h1>

<p>Get information about the user</p>

<h2 id="arguments">Arguments</h2>

<ul>
<li><code>verbose</code>: <code>bool</code>, Optional, determining level of information returned to the user</li>
<li><code>debug</code>: <code>bool</code>, Optional, determining level of information logged on the server</li>
</ul>

<h2 id="returns">Returns</h2>

<ul>
<li><code>dict</code> containing user information</li>
</ul>

<h2 id="example">Example</h2>

<div class="pdoc-code codehilite">
<pre><span></span><code><span class="kn">import</span> <span class="nn">twinlab</span> <span class="k">as</span> <span class="nn">tl</span>

<span class="n">user_info</span> <span class="o">=</span> <span class="n">tl</span><span class="o">.</span><span class="n">get_user_information</span><span class="p">()</span>
<span class="nb">print</span><span class="p">(</span><span class="n">user_info</span><span class="p">)</span>
</code></pre>
</div>
</div>


                </section>
                <section id="get_versions">
                            <input id="get_versions-view-source" class="view-source-toggle-state" type="checkbox" aria-hidden="true" tabindex="-1">
<div class="attr function">
            
        <span class="def">def</span>
        <span class="name">get_versions</span><span class="signature pdoc-code condensed">(<span class="param"><span class="n">verbose</span><span class="p">:</span> <span class="n">Optional</span><span class="p">[</span><span class="nb">bool</span><span class="p">]</span> <span class="o">=</span> <span class="kc">False</span>, </span><span class="param"><span class="n">debug</span><span class="p">:</span> <span class="n">Optional</span><span class="p">[</span><span class="nb">bool</span><span class="p">]</span> <span class="o">=</span> <span class="kc">False</span></span><span class="return-annotation">) -> <span class="nb">dict</span>:</span></span>

                <label class="view-source-button" for="get_versions-view-source"><span>View Source</span></label>

    </div>
    <a class="headerlink" href="#get_versions"></a>
            <div class="pdoc-code codehilite"><pre><span></span><span id="get_versions-137"><a href="#get_versions-137"><span class="linenos">137</span></a><span class="k">def</span> <span class="nf">get_versions</span><span class="p">(</span>
</span><span id="get_versions-138"><a href="#get_versions-138"><span class="linenos">138</span></a>    <span class="n">verbose</span><span class="p">:</span> <span class="n">Optional</span><span class="p">[</span><span class="nb">bool</span><span class="p">]</span> <span class="o">=</span> <span class="kc">False</span><span class="p">,</span> <span class="n">debug</span><span class="p">:</span> <span class="n">Optional</span><span class="p">[</span><span class="nb">bool</span><span class="p">]</span> <span class="o">=</span> <span class="kc">False</span>
</span><span id="get_versions-139"><a href="#get_versions-139"><span class="linenos">139</span></a><span class="p">)</span> <span class="o">-&gt;</span> <span class="nb">dict</span><span class="p">:</span>
</span><span id="get_versions-140"><a href="#get_versions-140"><span class="linenos">140</span></a><span class="w">    </span><span class="sd">&quot;&quot;&quot;</span>
</span><span id="get_versions-141"><a href="#get_versions-141"><span class="linenos">141</span></a><span class="sd">    # Get versions</span>
</span><span id="get_versions-142"><a href="#get_versions-142"><span class="linenos">142</span></a>
</span><span id="get_versions-143"><a href="#get_versions-143"><span class="linenos">143</span></a><span class="sd">    Get information about the twinLab version being used</span>
</span><span id="get_versions-144"><a href="#get_versions-144"><span class="linenos">144</span></a>
</span><span id="get_versions-145"><a href="#get_versions-145"><span class="linenos">145</span></a><span class="sd">    ## Arguments</span>
</span><span id="get_versions-146"><a href="#get_versions-146"><span class="linenos">146</span></a>
</span><span id="get_versions-147"><a href="#get_versions-147"><span class="linenos">147</span></a><span class="sd">    - `verbose`: `bool`, Optional, determining level of information returned to the user</span>
</span><span id="get_versions-148"><a href="#get_versions-148"><span class="linenos">148</span></a><span class="sd">    - `debug`: `bool`, Optional, determining level of information logged on the server</span>
</span><span id="get_versions-149"><a href="#get_versions-149"><span class="linenos">149</span></a>
</span><span id="get_versions-150"><a href="#get_versions-150"><span class="linenos">150</span></a><span class="sd">    ## Returns</span>
</span><span id="get_versions-151"><a href="#get_versions-151"><span class="linenos">151</span></a>
</span><span id="get_versions-152"><a href="#get_versions-152"><span class="linenos">152</span></a><span class="sd">    - `dict` containing version information</span>
</span><span id="get_versions-153"><a href="#get_versions-153"><span class="linenos">153</span></a>
</span><span id="get_versions-154"><a href="#get_versions-154"><span class="linenos">154</span></a><span class="sd">    ## Example</span>
</span><span id="get_versions-155"><a href="#get_versions-155"><span class="linenos">155</span></a><span class="sd">    ```python</span>
</span><span id="get_versions-156"><a href="#get_versions-156"><span class="linenos">156</span></a><span class="sd">    import twinlab as tl</span>
</span><span id="get_versions-157"><a href="#get_versions-157"><span class="linenos">157</span></a>
</span><span id="get_versions-158"><a href="#get_versions-158"><span class="linenos">158</span></a><span class="sd">    version_info = tl.get_versions()</span>
</span><span id="get_versions-159"><a href="#get_versions-159"><span class="linenos">159</span></a><span class="sd">    print(version_info)</span>
</span><span id="get_versions-160"><a href="#get_versions-160"><span class="linenos">160</span></a><span class="sd">    ```</span>
</span><span id="get_versions-161"><a href="#get_versions-161"><span class="linenos">161</span></a><span class="sd">    &quot;&quot;&quot;</span>
</span><span id="get_versions-162"><a href="#get_versions-162"><span class="linenos">162</span></a>    <span class="n">response</span> <span class="o">=</span> <span class="n">api</span><span class="o">.</span><span class="n">get_versions</span><span class="p">(</span><span class="n">verbose</span><span class="o">=</span><span class="n">debug</span><span class="p">)</span>
</span><span id="get_versions-163"><a href="#get_versions-163"><span class="linenos">163</span></a>    <span class="n">version_info</span> <span class="o">=</span> <span class="n">response</span>
</span><span id="get_versions-164"><a href="#get_versions-164"><span class="linenos">164</span></a>    <span class="k">if</span> <span class="n">verbose</span><span class="p">:</span>
</span><span id="get_versions-165"><a href="#get_versions-165"><span class="linenos">165</span></a>        <span class="nb">print</span><span class="p">(</span><span class="s2">&quot;Version information:&quot;</span><span class="p">)</span>
</span><span id="get_versions-166"><a href="#get_versions-166"><span class="linenos">166</span></a>        <span class="n">pprint</span><span class="p">(</span><span class="n">version_info</span><span class="p">,</span> <span class="n">compact</span><span class="o">=</span><span class="kc">True</span><span class="p">,</span> <span class="n">sort_dicts</span><span class="o">=</span><span class="kc">False</span><span class="p">)</span>
</span><span id="get_versions-167"><a href="#get_versions-167"><span class="linenos">167</span></a>    <span class="k">return</span> <span class="n">version_info</span>
</span></pre></div>


            <div class="docstring"><h1 id="get-versions">Get versions</h1>

<p>Get information about the twinLab version being used</p>

<h2 id="arguments">Arguments</h2>

<ul>
<li><code>verbose</code>: <code>bool</code>, Optional, determining level of information returned to the user</li>
<li><code>debug</code>: <code>bool</code>, Optional, determining level of information logged on the server</li>
</ul>

<h2 id="returns">Returns</h2>

<ul>
<li><code>dict</code> containing version information</li>
</ul>

<h2 id="example">Example</h2>

<div class="pdoc-code codehilite">
<pre><span></span><code><span class="kn">import</span> <span class="nn">twinlab</span> <span class="k">as</span> <span class="nn">tl</span>

<span class="n">version_info</span> <span class="o">=</span> <span class="n">tl</span><span class="o">.</span><span class="n">get_versions</span><span class="p">()</span>
<span class="nb">print</span><span class="p">(</span><span class="n">version_info</span><span class="p">)</span>
</code></pre>
</div>
</div>


                </section>
                <section id="upload_dataset">
                            <input id="upload_dataset-view-source" class="view-source-toggle-state" type="checkbox" aria-hidden="true" tabindex="-1">
<div class="attr function">
            
        <span class="def">def</span>
        <span class="name">upload_dataset</span><span class="signature pdoc-code multiline">(<span class="param">	<span class="n">filepath_or_df</span><span class="p">:</span> <span class="n">Union</span><span class="p">[</span><span class="nb">str</span><span class="p">,</span> <span class="n">pandas</span><span class="o">.</span><span class="n">core</span><span class="o">.</span><span class="n">frame</span><span class="o">.</span><span class="n">DataFrame</span><span class="p">]</span>,</span><span class="param">	<span class="n">dataset_id</span><span class="p">:</span> <span class="nb">str</span>,</span><span class="param">	<span class="n">use_upload_url</span><span class="p">:</span> <span class="n">Optional</span><span class="p">[</span><span class="nb">bool</span><span class="p">]</span> <span class="o">=</span> <span class="kc">True</span>,</span><span class="param">	<span class="n">verbose</span><span class="p">:</span> <span class="n">Optional</span><span class="p">[</span><span class="nb">bool</span><span class="p">]</span> <span class="o">=</span> <span class="kc">False</span>,</span><span class="param">	<span class="n">debug</span><span class="p">:</span> <span class="n">Optional</span><span class="p">[</span><span class="nb">bool</span><span class="p">]</span> <span class="o">=</span> <span class="kc">False</span></span><span class="return-annotation">) -> <span class="kc">None</span>:</span></span>

                <label class="view-source-button" for="upload_dataset-view-source"><span>View Source</span></label>

    </div>
    <a class="headerlink" href="#upload_dataset"></a>
            <div class="pdoc-code codehilite"><pre><span></span><span id="upload_dataset-176"><a href="#upload_dataset-176"><span class="linenos">176</span></a><span class="k">def</span> <span class="nf">upload_dataset</span><span class="p">(</span>
</span><span id="upload_dataset-177"><a href="#upload_dataset-177"><span class="linenos">177</span></a>    <span class="n">filepath_or_df</span><span class="p">:</span> <span class="n">Union</span><span class="p">[</span><span class="nb">str</span><span class="p">,</span> <span class="n">pd</span><span class="o">.</span><span class="n">DataFrame</span><span class="p">],</span>
</span><span id="upload_dataset-178"><a href="#upload_dataset-178"><span class="linenos">178</span></a>    <span class="n">dataset_id</span><span class="p">:</span> <span class="nb">str</span><span class="p">,</span>
</span><span id="upload_dataset-179"><a href="#upload_dataset-179"><span class="linenos">179</span></a>    <span class="n">use_upload_url</span><span class="p">:</span> <span class="n">Optional</span><span class="p">[</span><span class="nb">bool</span><span class="p">]</span> <span class="o">=</span> <span class="kc">True</span><span class="p">,</span>
</span><span id="upload_dataset-180"><a href="#upload_dataset-180"><span class="linenos">180</span></a>    <span class="n">verbose</span><span class="p">:</span> <span class="n">Optional</span><span class="p">[</span><span class="nb">bool</span><span class="p">]</span> <span class="o">=</span> <span class="kc">False</span><span class="p">,</span>
</span><span id="upload_dataset-181"><a href="#upload_dataset-181"><span class="linenos">181</span></a>    <span class="n">debug</span><span class="p">:</span> <span class="n">Optional</span><span class="p">[</span><span class="nb">bool</span><span class="p">]</span> <span class="o">=</span> <span class="kc">False</span><span class="p">,</span>
</span><span id="upload_dataset-182"><a href="#upload_dataset-182"><span class="linenos">182</span></a><span class="p">)</span> <span class="o">-&gt;</span> <span class="kc">None</span><span class="p">:</span>
</span><span id="upload_dataset-183"><a href="#upload_dataset-183"><span class="linenos">183</span></a><span class="w">    </span><span class="sd">&quot;&quot;&quot;</span>
</span><span id="upload_dataset-184"><a href="#upload_dataset-184"><span class="linenos">184</span></a><span class="sd">    # Upload dataset</span>
</span><span id="upload_dataset-185"><a href="#upload_dataset-185"><span class="linenos">185</span></a>
</span><span id="upload_dataset-186"><a href="#upload_dataset-186"><span class="linenos">186</span></a><span class="sd">    Upload a dataset to the `twinLab` cloud so that it can be queried and used for training.</span>
</span><span id="upload_dataset-187"><a href="#upload_dataset-187"><span class="linenos">187</span></a>
</span><span id="upload_dataset-188"><a href="#upload_dataset-188"><span class="linenos">188</span></a><span class="sd">    ## Arguments</span>
</span><span id="upload_dataset-189"><a href="#upload_dataset-189"><span class="linenos">189</span></a>
</span><span id="upload_dataset-190"><a href="#upload_dataset-190"><span class="linenos">190</span></a><span class="sd">    - `filepath_or_df`: `str` | `Dataframe`, location of csv dataset on local machine or `pandas` dataframe</span>
</span><span id="upload_dataset-191"><a href="#upload_dataset-191"><span class="linenos">191</span></a><span class="sd">    - `dataset_id`: `str`, name for the dataset when saved to the twinLab cloud</span>
</span><span id="upload_dataset-192"><a href="#upload_dataset-192"><span class="linenos">192</span></a><span class="sd">    **Warning:** If the `dataset_id` already exists for the current cloud account, it will be overwritten by the</span>
</span><span id="upload_dataset-193"><a href="#upload_dataset-193"><span class="linenos">193</span></a><span class="sd">    newly uploaded dataset</span>
</span><span id="upload_dataset-194"><a href="#upload_dataset-194"><span class="linenos">194</span></a><span class="sd">    - `use_upload_url`: `bool`, Optional, determining whether to upload via a pre-signed url or directly to the server</span>
</span><span id="upload_dataset-195"><a href="#upload_dataset-195"><span class="linenos">195</span></a><span class="sd">    - `verbose`: `bool`, Optional, determining level of information returned to the user</span>
</span><span id="upload_dataset-196"><a href="#upload_dataset-196"><span class="linenos">196</span></a><span class="sd">    - `debug`: `bool`, Optional,determining level of information logged on the server</span>
</span><span id="upload_dataset-197"><a href="#upload_dataset-197"><span class="linenos">197</span></a>
</span><span id="upload_dataset-198"><a href="#upload_dataset-198"><span class="linenos">198</span></a><span class="sd">    **NOTE:** Local data must be a CSV file, working data should be a pandas Dataframe.</span>
</span><span id="upload_dataset-199"><a href="#upload_dataset-199"><span class="linenos">199</span></a>
</span><span id="upload_dataset-200"><a href="#upload_dataset-200"><span class="linenos">200</span></a><span class="sd">    ## Examples</span>
</span><span id="upload_dataset-201"><a href="#upload_dataset-201"><span class="linenos">201</span></a>
</span><span id="upload_dataset-202"><a href="#upload_dataset-202"><span class="linenos">202</span></a><span class="sd">    Upload a local file:</span>
</span><span id="upload_dataset-203"><a href="#upload_dataset-203"><span class="linenos">203</span></a><span class="sd">    ```python</span>
</span><span id="upload_dataset-204"><a href="#upload_dataset-204"><span class="linenos">204</span></a><span class="sd">    import twinlab as tl</span>
</span><span id="upload_dataset-205"><a href="#upload_dataset-205"><span class="linenos">205</span></a>
</span><span id="upload_dataset-206"><a href="#upload_dataset-206"><span class="linenos">206</span></a><span class="sd">    data_filepath = &quot;path/to/dataset.csv&quot;</span>
</span><span id="upload_dataset-207"><a href="#upload_dataset-207"><span class="linenos">207</span></a><span class="sd">    tl.upload_dataset(data_filepath, &quot;my_dataset&quot;)</span>
</span><span id="upload_dataset-208"><a href="#upload_dataset-208"><span class="linenos">208</span></a><span class="sd">    ```</span>
</span><span id="upload_dataset-209"><a href="#upload_dataset-209"><span class="linenos">209</span></a>
</span><span id="upload_dataset-210"><a href="#upload_dataset-210"><span class="linenos">210</span></a><span class="sd">    Upload a `pandas` dataframe:</span>
</span><span id="upload_dataset-211"><a href="#upload_dataset-211"><span class="linenos">211</span></a><span class="sd">    ```python</span>
</span><span id="upload_dataset-212"><a href="#upload_dataset-212"><span class="linenos">212</span></a><span class="sd">    import pandas as pd</span>
</span><span id="upload_dataset-213"><a href="#upload_dataset-213"><span class="linenos">213</span></a><span class="sd">    import twinlab as tl</span>
</span><span id="upload_dataset-214"><a href="#upload_dataset-214"><span class="linenos">214</span></a>
</span><span id="upload_dataset-215"><a href="#upload_dataset-215"><span class="linenos">215</span></a><span class="sd">    df = pd.DataFrame({&#39;X&#39;: [1, 2, 3, 4], &#39;y&#39;: [1, 4, 9, 16]})</span>
</span><span id="upload_dataset-216"><a href="#upload_dataset-216"><span class="linenos">216</span></a><span class="sd">    tl.upload_dataset(df, &quot;my_dataset&quot;)</span>
</span><span id="upload_dataset-217"><a href="#upload_dataset-217"><span class="linenos">217</span></a><span class="sd">    ```</span>
</span><span id="upload_dataset-218"><a href="#upload_dataset-218"><span class="linenos">218</span></a><span class="sd">    &quot;&quot;&quot;</span>
</span><span id="upload_dataset-219"><a href="#upload_dataset-219"><span class="linenos">219</span></a>
</span><span id="upload_dataset-220"><a href="#upload_dataset-220"><span class="linenos">220</span></a>    <span class="c1"># Upload the file (either via link or directly)</span>
</span><span id="upload_dataset-221"><a href="#upload_dataset-221"><span class="linenos">221</span></a>    <span class="k">if</span> <span class="n">use_upload_url</span><span class="p">:</span>
</span><span id="upload_dataset-222"><a href="#upload_dataset-222"><span class="linenos">222</span></a>        <span class="n">response</span> <span class="o">=</span> <span class="n">api</span><span class="o">.</span><span class="n">generate_upload_url</span><span class="p">(</span><span class="n">dataset_id</span><span class="p">,</span> <span class="n">verbose</span><span class="o">=</span><span class="n">debug</span><span class="p">)</span>
</span><span id="upload_dataset-223"><a href="#upload_dataset-223"><span class="linenos">223</span></a>        <span class="n">upload_url</span> <span class="o">=</span> <span class="n">get_value_from_body</span><span class="p">(</span><span class="s2">&quot;url&quot;</span><span class="p">,</span> <span class="n">response</span><span class="p">)</span>
</span><span id="upload_dataset-224"><a href="#upload_dataset-224"><span class="linenos">224</span></a>        <span class="k">if</span> <span class="nb">type</span><span class="p">(</span><span class="n">filepath_or_df</span><span class="p">)</span> <span class="ow">is</span> <span class="nb">str</span><span class="p">:</span>
</span><span id="upload_dataset-225"><a href="#upload_dataset-225"><span class="linenos">225</span></a>            <span class="n">filepath</span> <span class="o">=</span> <span class="n">filepath_or_df</span>
</span><span id="upload_dataset-226"><a href="#upload_dataset-226"><span class="linenos">226</span></a>            <span class="n">utils</span><span class="o">.</span><span class="n">upload_file_to_presigned_url</span><span class="p">(</span>
</span><span id="upload_dataset-227"><a href="#upload_dataset-227"><span class="linenos">227</span></a>                <span class="n">filepath</span><span class="p">,</span> <span class="n">upload_url</span><span class="p">,</span> <span class="n">verbose</span><span class="o">=</span><span class="n">verbose</span><span class="p">,</span> <span class="n">check</span><span class="o">=</span><span class="n">settings</span><span class="o">.</span><span class="n">CHECK_DATASETS</span>
</span><span id="upload_dataset-228"><a href="#upload_dataset-228"><span class="linenos">228</span></a>            <span class="p">)</span>
</span><span id="upload_dataset-229"><a href="#upload_dataset-229"><span class="linenos">229</span></a>        <span class="k">elif</span> <span class="nb">type</span><span class="p">(</span><span class="n">filepath_or_df</span><span class="p">)</span> <span class="ow">is</span> <span class="n">pd</span><span class="o">.</span><span class="n">DataFrame</span><span class="p">:</span>
</span><span id="upload_dataset-230"><a href="#upload_dataset-230"><span class="linenos">230</span></a>            <span class="n">df</span> <span class="o">=</span> <span class="n">filepath_or_df</span>
</span><span id="upload_dataset-231"><a href="#upload_dataset-231"><span class="linenos">231</span></a>            <span class="n">utils</span><span class="o">.</span><span class="n">upload_dataframe_to_presigned_url</span><span class="p">(</span>
</span><span id="upload_dataset-232"><a href="#upload_dataset-232"><span class="linenos">232</span></a>                <span class="n">df</span><span class="p">,</span> <span class="n">upload_url</span><span class="p">,</span> <span class="n">verbose</span><span class="o">=</span><span class="n">verbose</span><span class="p">,</span> <span class="n">check</span><span class="o">=</span><span class="n">settings</span><span class="o">.</span><span class="n">CHECK_DATASETS</span>
</span><span id="upload_dataset-233"><a href="#upload_dataset-233"><span class="linenos">233</span></a>            <span class="p">)</span>
</span><span id="upload_dataset-234"><a href="#upload_dataset-234"><span class="linenos">234</span></a>        <span class="k">else</span><span class="p">:</span>
</span><span id="upload_dataset-235"><a href="#upload_dataset-235"><span class="linenos">235</span></a>            <span class="k">raise</span> <span class="ne">ValueError</span><span class="p">(</span><span class="s2">&quot;filepath_or_df must be a string or pandas dataframe&quot;</span><span class="p">)</span>
</span><span id="upload_dataset-236"><a href="#upload_dataset-236"><span class="linenos">236</span></a>        <span class="k">if</span> <span class="n">verbose</span><span class="p">:</span>
</span><span id="upload_dataset-237"><a href="#upload_dataset-237"><span class="linenos">237</span></a>            <span class="nb">print</span><span class="p">(</span><span class="s2">&quot;Processing dataset.&quot;</span><span class="p">)</span>
</span><span id="upload_dataset-238"><a href="#upload_dataset-238"><span class="linenos">238</span></a>        <span class="n">response</span> <span class="o">=</span> <span class="n">api</span><span class="o">.</span><span class="n">process_uploaded_dataset</span><span class="p">(</span><span class="n">dataset_id</span><span class="p">,</span> <span class="n">verbose</span><span class="o">=</span><span class="n">debug</span><span class="p">)</span>
</span><span id="upload_dataset-239"><a href="#upload_dataset-239"><span class="linenos">239</span></a>
</span><span id="upload_dataset-240"><a href="#upload_dataset-240"><span class="linenos">240</span></a>    <span class="k">else</span><span class="p">:</span>
</span><span id="upload_dataset-241"><a href="#upload_dataset-241"><span class="linenos">241</span></a>        <span class="n">csv_string</span> <span class="o">=</span> <span class="n">_get_csv_string</span><span class="p">(</span><span class="n">filepath_or_df</span><span class="p">)</span>
</span><span id="upload_dataset-242"><a href="#upload_dataset-242"><span class="linenos">242</span></a>        <span class="n">response</span> <span class="o">=</span> <span class="n">api</span><span class="o">.</span><span class="n">upload_dataset</span><span class="p">(</span><span class="n">dataset_id</span><span class="p">,</span> <span class="n">csv_string</span><span class="p">,</span> <span class="n">verbose</span><span class="o">=</span><span class="n">debug</span><span class="p">)</span>
</span><span id="upload_dataset-243"><a href="#upload_dataset-243"><span class="linenos">243</span></a>
</span><span id="upload_dataset-244"><a href="#upload_dataset-244"><span class="linenos">244</span></a>    <span class="k">if</span> <span class="n">verbose</span><span class="p">:</span>
</span><span id="upload_dataset-245"><a href="#upload_dataset-245"><span class="linenos">245</span></a>        <span class="n">message</span> <span class="o">=</span> <span class="n">_get_message</span><span class="p">(</span><span class="n">response</span><span class="p">)</span>
</span><span id="upload_dataset-246"><a href="#upload_dataset-246"><span class="linenos">246</span></a>        <span class="nb">print</span><span class="p">(</span><span class="n">message</span><span class="p">)</span>
</span></pre></div>


            <div class="docstring"><h1 id="upload-dataset">Upload dataset</h1>

<p>Upload a dataset to the <code>twinLab</code> cloud so that it can be queried and used for training.</p>

<h2 id="arguments">Arguments</h2>

<ul>
<li><code>filepath_or_df</code>: <code>str</code> | <code>Dataframe</code>, location of csv dataset on local machine or <code>pandas</code> dataframe</li>
<li><code>dataset_id</code>: <code>str</code>, name for the dataset when saved to the twinLab cloud
<strong>Warning:</strong> If the <code>dataset_id</code> already exists for the current cloud account, it will be overwritten by the
newly uploaded dataset</li>
<li><code>use_upload_url</code>: <code>bool</code>, Optional, determining whether to upload via a pre-signed url or directly to the server</li>
<li><code>verbose</code>: <code>bool</code>, Optional, determining level of information returned to the user</li>
<li><code>debug</code>: <code>bool</code>, Optional,determining level of information logged on the server</li>
</ul>

<p><strong>NOTE:</strong> Local data must be a CSV file, working data should be a pandas Dataframe.</p>

<h2 id="examples">Examples</h2>

<p>Upload a local file:</p>

<div class="pdoc-code codehilite">
<pre><span></span><code><span class="kn">import</span> <span class="nn">twinlab</span> <span class="k">as</span> <span class="nn">tl</span>

<span class="n">data_filepath</span> <span class="o">=</span> <span class="s2">&quot;path/to/dataset.csv&quot;</span>
<span class="n">tl</span><span class="o">.</span><span class="n">upload_dataset</span><span class="p">(</span><span class="n">data_filepath</span><span class="p">,</span> <span class="s2">&quot;my_dataset&quot;</span><span class="p">)</span>
</code></pre>
</div>

<p>Upload a <code>pandas</code> dataframe:</p>

<div class="pdoc-code codehilite">
<pre><span></span><code><span class="kn">import</span> <span class="nn">pandas</span> <span class="k">as</span> <span class="nn">pd</span>
<span class="kn">import</span> <span class="nn">twinlab</span> <span class="k">as</span> <span class="nn">tl</span>

<span class="n">df</span> <span class="o">=</span> <span class="n">pd</span><span class="o">.</span><span class="n">DataFrame</span><span class="p">({</span><span class="s1">&#39;X&#39;</span><span class="p">:</span> <span class="p">[</span><span class="mi">1</span><span class="p">,</span> <span class="mi">2</span><span class="p">,</span> <span class="mi">3</span><span class="p">,</span> <span class="mi">4</span><span class="p">],</span> <span class="s1">&#39;y&#39;</span><span class="p">:</span> <span class="p">[</span><span class="mi">1</span><span class="p">,</span> <span class="mi">4</span><span class="p">,</span> <span class="mi">9</span><span class="p">,</span> <span class="mi">16</span><span class="p">]})</span>
<span class="n">tl</span><span class="o">.</span><span class="n">upload_dataset</span><span class="p">(</span><span class="n">df</span><span class="p">,</span> <span class="s2">&quot;my_dataset&quot;</span><span class="p">)</span>
</code></pre>
</div>
</div>


                </section>
                <section id="list_datasets">
                            <input id="list_datasets-view-source" class="view-source-toggle-state" type="checkbox" aria-hidden="true" tabindex="-1">
<div class="attr function">
            
        <span class="def">def</span>
        <span class="name">list_datasets</span><span class="signature pdoc-code condensed">(<span class="param"><span class="n">verbose</span><span class="p">:</span> <span class="n">Optional</span><span class="p">[</span><span class="nb">bool</span><span class="p">]</span> <span class="o">=</span> <span class="kc">False</span>, </span><span class="param"><span class="n">debug</span><span class="p">:</span> <span class="n">Optional</span><span class="p">[</span><span class="nb">bool</span><span class="p">]</span> <span class="o">=</span> <span class="kc">False</span></span><span class="return-annotation">) -> <span class="nb">list</span>:</span></span>

                <label class="view-source-button" for="list_datasets-view-source"><span>View Source</span></label>

    </div>
    <a class="headerlink" href="#list_datasets"></a>
            <div class="pdoc-code codehilite"><pre><span></span><span id="list_datasets-250"><a href="#list_datasets-250"><span class="linenos">250</span></a><span class="k">def</span> <span class="nf">list_datasets</span><span class="p">(</span>
</span><span id="list_datasets-251"><a href="#list_datasets-251"><span class="linenos">251</span></a>    <span class="n">verbose</span><span class="p">:</span> <span class="n">Optional</span><span class="p">[</span><span class="nb">bool</span><span class="p">]</span> <span class="o">=</span> <span class="kc">False</span><span class="p">,</span> <span class="n">debug</span><span class="p">:</span> <span class="n">Optional</span><span class="p">[</span><span class="nb">bool</span><span class="p">]</span> <span class="o">=</span> <span class="kc">False</span>
</span><span id="list_datasets-252"><a href="#list_datasets-252"><span class="linenos">252</span></a><span class="p">)</span> <span class="o">-&gt;</span> <span class="nb">list</span><span class="p">:</span>
</span><span id="list_datasets-253"><a href="#list_datasets-253"><span class="linenos">253</span></a><span class="w">    </span><span class="sd">&quot;&quot;&quot;</span>
</span><span id="list_datasets-254"><a href="#list_datasets-254"><span class="linenos">254</span></a><span class="sd">    # List datasets</span>
</span><span id="list_datasets-255"><a href="#list_datasets-255"><span class="linenos">255</span></a>
</span><span id="list_datasets-256"><a href="#list_datasets-256"><span class="linenos">256</span></a><span class="sd">    List datasets that have been uploaded to the `twinLab` cloud</span>
</span><span id="list_datasets-257"><a href="#list_datasets-257"><span class="linenos">257</span></a>
</span><span id="list_datasets-258"><a href="#list_datasets-258"><span class="linenos">258</span></a><span class="sd">    ## Arguments</span>
</span><span id="list_datasets-259"><a href="#list_datasets-259"><span class="linenos">259</span></a>
</span><span id="list_datasets-260"><a href="#list_datasets-260"><span class="linenos">260</span></a><span class="sd">    - `verbose`: `bool`, Optional, determining level of information returned to the user</span>
</span><span id="list_datasets-261"><a href="#list_datasets-261"><span class="linenos">261</span></a><span class="sd">    - `debug`: `bool`, Optional, determining level of information logged on the server</span>
</span><span id="list_datasets-262"><a href="#list_datasets-262"><span class="linenos">262</span></a>
</span><span id="list_datasets-263"><a href="#list_datasets-263"><span class="linenos">263</span></a><span class="sd">    ## Returns</span>
</span><span id="list_datasets-264"><a href="#list_datasets-264"><span class="linenos">264</span></a>
</span><span id="list_datasets-265"><a href="#list_datasets-265"><span class="linenos">265</span></a><span class="sd">    - `list` of `str` dataset ids</span>
</span><span id="list_datasets-266"><a href="#list_datasets-266"><span class="linenos">266</span></a>
</span><span id="list_datasets-267"><a href="#list_datasets-267"><span class="linenos">267</span></a><span class="sd">    ## Example</span>
</span><span id="list_datasets-268"><a href="#list_datasets-268"><span class="linenos">268</span></a>
</span><span id="list_datasets-269"><a href="#list_datasets-269"><span class="linenos">269</span></a><span class="sd">    ```python</span>
</span><span id="list_datasets-270"><a href="#list_datasets-270"><span class="linenos">270</span></a><span class="sd">    import pandas as pd</span>
</span><span id="list_datasets-271"><a href="#list_datasets-271"><span class="linenos">271</span></a><span class="sd">    import twinlab as tl</span>
</span><span id="list_datasets-272"><a href="#list_datasets-272"><span class="linenos">272</span></a>
</span><span id="list_datasets-273"><a href="#list_datasets-273"><span class="linenos">273</span></a><span class="sd">    datasets = tl.list_datasets()</span>
</span><span id="list_datasets-274"><a href="#list_datasets-274"><span class="linenos">274</span></a><span class="sd">    print(datasets)</span>
</span><span id="list_datasets-275"><a href="#list_datasets-275"><span class="linenos">275</span></a><span class="sd">    ```</span>
</span><span id="list_datasets-276"><a href="#list_datasets-276"><span class="linenos">276</span></a><span class="sd">    &quot;&quot;&quot;</span>
</span><span id="list_datasets-277"><a href="#list_datasets-277"><span class="linenos">277</span></a>    <span class="n">response</span> <span class="o">=</span> <span class="n">api</span><span class="o">.</span><span class="n">list_datasets</span><span class="p">(</span><span class="n">verbose</span><span class="o">=</span><span class="n">debug</span><span class="p">)</span>
</span><span id="list_datasets-278"><a href="#list_datasets-278"><span class="linenos">278</span></a>    <span class="n">datasets</span> <span class="o">=</span> <span class="n">get_value_from_body</span><span class="p">(</span><span class="s2">&quot;datasets&quot;</span><span class="p">,</span> <span class="n">response</span><span class="p">)</span>
</span><span id="list_datasets-279"><a href="#list_datasets-279"><span class="linenos">279</span></a>    <span class="k">if</span> <span class="n">verbose</span><span class="p">:</span>
</span><span id="list_datasets-280"><a href="#list_datasets-280"><span class="linenos">280</span></a>        <span class="nb">print</span><span class="p">(</span><span class="s2">&quot;Datasets:&quot;</span><span class="p">)</span>
</span><span id="list_datasets-281"><a href="#list_datasets-281"><span class="linenos">281</span></a>        <span class="n">pprint</span><span class="p">(</span><span class="n">datasets</span><span class="p">,</span> <span class="n">compact</span><span class="o">=</span><span class="kc">True</span><span class="p">,</span> <span class="n">sort_dicts</span><span class="o">=</span><span class="kc">False</span><span class="p">)</span>
</span><span id="list_datasets-282"><a href="#list_datasets-282"><span class="linenos">282</span></a>    <span class="k">return</span> <span class="n">datasets</span>
</span><span id="list_datasets-283"><a href="#list_datasets-283"><span class="linenos">283</span></a>
</span><span id="list_datasets-284"><a href="#list_datasets-284"><span class="linenos">284</span></a>    <span class="c1"># try:</span>
</span><span id="list_datasets-285"><a href="#list_datasets-285"><span class="linenos">285</span></a>    <span class="c1">#     datasets = get_value_from_body(&quot;datasets&quot;, response)</span>
</span><span id="list_datasets-286"><a href="#list_datasets-286"><span class="linenos">286</span></a>    <span class="c1">#     if verbose:</span>
</span><span id="list_datasets-287"><a href="#list_datasets-287"><span class="linenos">287</span></a>    <span class="c1">#         print(&quot;Datasets:&quot;)</span>
</span><span id="list_datasets-288"><a href="#list_datasets-288"><span class="linenos">288</span></a>    <span class="c1">#         pprint(datasets, compact=True, sort_dicts=False)</span>
</span><span id="list_datasets-289"><a href="#list_datasets-289"><span class="linenos">289</span></a>    <span class="c1">#     return datasets</span>
</span><span id="list_datasets-290"><a href="#list_datasets-290"><span class="linenos">290</span></a>    <span class="c1"># except:</span>
</span><span id="list_datasets-291"><a href="#list_datasets-291"><span class="linenos">291</span></a>    <span class="c1">#     print(response)</span>
</span></pre></div>


            <div class="docstring"><h1 id="list-datasets">List datasets</h1>

<p>List datasets that have been uploaded to the <code>twinLab</code> cloud</p>

<h2 id="arguments">Arguments</h2>

<ul>
<li><code>verbose</code>: <code>bool</code>, Optional, determining level of information returned to the user</li>
<li><code>debug</code>: <code>bool</code>, Optional, determining level of information logged on the server</li>
</ul>

<h2 id="returns">Returns</h2>

<ul>
<li><code>list</code> of <code>str</code> dataset ids</li>
</ul>

<h2 id="example">Example</h2>

<div class="pdoc-code codehilite">
<pre><span></span><code><span class="kn">import</span> <span class="nn">pandas</span> <span class="k">as</span> <span class="nn">pd</span>
<span class="kn">import</span> <span class="nn">twinlab</span> <span class="k">as</span> <span class="nn">tl</span>

<span class="n">datasets</span> <span class="o">=</span> <span class="n">tl</span><span class="o">.</span><span class="n">list_datasets</span><span class="p">()</span>
<span class="nb">print</span><span class="p">(</span><span class="n">datasets</span><span class="p">)</span>
</code></pre>
</div>
</div>


                </section>
                <section id="view_dataset">
                            <input id="view_dataset-view-source" class="view-source-toggle-state" type="checkbox" aria-hidden="true" tabindex="-1">
<div class="attr function">
            
        <span class="def">def</span>
        <span class="name">view_dataset</span><span class="signature pdoc-code multiline">(<span class="param">	<span class="n">dataset_id</span><span class="p">:</span> <span class="nb">str</span>,</span><span class="param">	<span class="n">verbose</span><span class="p">:</span> <span class="n">Optional</span><span class="p">[</span><span class="nb">bool</span><span class="p">]</span> <span class="o">=</span> <span class="kc">False</span>,</span><span class="param">	<span class="n">debug</span><span class="p">:</span> <span class="n">Optional</span><span class="p">[</span><span class="nb">bool</span><span class="p">]</span> <span class="o">=</span> <span class="kc">False</span></span><span class="return-annotation">) -> <span class="n">pandas</span><span class="o">.</span><span class="n">core</span><span class="o">.</span><span class="n">frame</span><span class="o">.</span><span class="n">DataFrame</span>:</span></span>

                <label class="view-source-button" for="view_dataset-view-source"><span>View Source</span></label>

    </div>
    <a class="headerlink" href="#view_dataset"></a>
            <div class="pdoc-code codehilite"><pre><span></span><span id="view_dataset-295"><a href="#view_dataset-295"><span class="linenos">295</span></a><span class="k">def</span> <span class="nf">view_dataset</span><span class="p">(</span>
</span><span id="view_dataset-296"><a href="#view_dataset-296"><span class="linenos">296</span></a>    <span class="n">dataset_id</span><span class="p">:</span> <span class="nb">str</span><span class="p">,</span> <span class="n">verbose</span><span class="p">:</span> <span class="n">Optional</span><span class="p">[</span><span class="nb">bool</span><span class="p">]</span> <span class="o">=</span> <span class="kc">False</span><span class="p">,</span> <span class="n">debug</span><span class="p">:</span> <span class="n">Optional</span><span class="p">[</span><span class="nb">bool</span><span class="p">]</span> <span class="o">=</span> <span class="kc">False</span>
</span><span id="view_dataset-297"><a href="#view_dataset-297"><span class="linenos">297</span></a><span class="p">)</span> <span class="o">-&gt;</span> <span class="n">pd</span><span class="o">.</span><span class="n">DataFrame</span><span class="p">:</span>
</span><span id="view_dataset-298"><a href="#view_dataset-298"><span class="linenos">298</span></a><span class="w">    </span><span class="sd">&quot;&quot;&quot;</span>
</span><span id="view_dataset-299"><a href="#view_dataset-299"><span class="linenos">299</span></a><span class="sd">    # View dataset</span>
</span><span id="view_dataset-300"><a href="#view_dataset-300"><span class="linenos">300</span></a>
</span><span id="view_dataset-301"><a href="#view_dataset-301"><span class="linenos">301</span></a><span class="sd">    View a dataset that exists on the twinLab cloud.</span>
</span><span id="view_dataset-302"><a href="#view_dataset-302"><span class="linenos">302</span></a>
</span><span id="view_dataset-303"><a href="#view_dataset-303"><span class="linenos">303</span></a><span class="sd">    ## Arguments</span>
</span><span id="view_dataset-304"><a href="#view_dataset-304"><span class="linenos">304</span></a>
</span><span id="view_dataset-305"><a href="#view_dataset-305"><span class="linenos">305</span></a><span class="sd">    - `dataset_id`: `str`; name for the dataset when saved to the twinLab cloud</span>
</span><span id="view_dataset-306"><a href="#view_dataset-306"><span class="linenos">306</span></a><span class="sd">    - `verbose`: `bool`, Optional, determining level of information returned to the user</span>
</span><span id="view_dataset-307"><a href="#view_dataset-307"><span class="linenos">307</span></a><span class="sd">    - `debug`: `bool`, Optional, determining level of information logged on the server</span>
</span><span id="view_dataset-308"><a href="#view_dataset-308"><span class="linenos">308</span></a>
</span><span id="view_dataset-309"><a href="#view_dataset-309"><span class="linenos">309</span></a><span class="sd">    ## Returns</span>
</span><span id="view_dataset-310"><a href="#view_dataset-310"><span class="linenos">310</span></a>
</span><span id="view_dataset-311"><a href="#view_dataset-311"><span class="linenos">311</span></a><span class="sd">    - `pandas.DataFrame` of the dataset.</span>
</span><span id="view_dataset-312"><a href="#view_dataset-312"><span class="linenos">312</span></a>
</span><span id="view_dataset-313"><a href="#view_dataset-313"><span class="linenos">313</span></a>
</span><span id="view_dataset-314"><a href="#view_dataset-314"><span class="linenos">314</span></a><span class="sd">    ## Example</span>
</span><span id="view_dataset-315"><a href="#view_dataset-315"><span class="linenos">315</span></a>
</span><span id="view_dataset-316"><a href="#view_dataset-316"><span class="linenos">316</span></a><span class="sd">    ```python</span>
</span><span id="view_dataset-317"><a href="#view_dataset-317"><span class="linenos">317</span></a><span class="sd">    import pandas as pd</span>
</span><span id="view_dataset-318"><a href="#view_dataset-318"><span class="linenos">318</span></a><span class="sd">    import twinlab as tl</span>
</span><span id="view_dataset-319"><a href="#view_dataset-319"><span class="linenos">319</span></a>
</span><span id="view_dataset-320"><a href="#view_dataset-320"><span class="linenos">320</span></a><span class="sd">    df = pd.DataFrame({&#39;X&#39;: [1, 2, 3, 4], &#39;y&#39;: [1, 4, 9, 16]})</span>
</span><span id="view_dataset-321"><a href="#view_dataset-321"><span class="linenos">321</span></a><span class="sd">    tl.upload_dataset(df, &quot;my_dataset&quot;)</span>
</span><span id="view_dataset-322"><a href="#view_dataset-322"><span class="linenos">322</span></a><span class="sd">    df = tl.view_dataset(&quot;my_dataset&quot;)</span>
</span><span id="view_dataset-323"><a href="#view_dataset-323"><span class="linenos">323</span></a><span class="sd">    print(df)</span>
</span><span id="view_dataset-324"><a href="#view_dataset-324"><span class="linenos">324</span></a><span class="sd">    ```</span>
</span><span id="view_dataset-325"><a href="#view_dataset-325"><span class="linenos">325</span></a><span class="sd">    &quot;&quot;&quot;</span>
</span><span id="view_dataset-326"><a href="#view_dataset-326"><span class="linenos">326</span></a>    <span class="n">response</span> <span class="o">=</span> <span class="n">api</span><span class="o">.</span><span class="n">view_dataset</span><span class="p">(</span><span class="n">dataset_id</span><span class="p">,</span> <span class="n">verbose</span><span class="o">=</span><span class="n">debug</span><span class="p">)</span>
</span><span id="view_dataset-327"><a href="#view_dataset-327"><span class="linenos">327</span></a>    <span class="n">csv_string</span> <span class="o">=</span> <span class="n">get_value_from_body</span><span class="p">(</span><span class="s2">&quot;dataset&quot;</span><span class="p">,</span> <span class="n">response</span><span class="p">)</span>
</span><span id="view_dataset-328"><a href="#view_dataset-328"><span class="linenos">328</span></a>    <span class="n">csv_string</span> <span class="o">=</span> <span class="n">io</span><span class="o">.</span><span class="n">StringIO</span><span class="p">(</span><span class="n">csv_string</span><span class="p">)</span>
</span><span id="view_dataset-329"><a href="#view_dataset-329"><span class="linenos">329</span></a>    <span class="n">df</span> <span class="o">=</span> <span class="n">pd</span><span class="o">.</span><span class="n">read_csv</span><span class="p">(</span><span class="n">csv_string</span><span class="p">,</span> <span class="n">sep</span><span class="o">=</span><span class="s2">&quot;,&quot;</span><span class="p">)</span>
</span><span id="view_dataset-330"><a href="#view_dataset-330"><span class="linenos">330</span></a>    <span class="k">if</span> <span class="n">verbose</span><span class="p">:</span>
</span><span id="view_dataset-331"><a href="#view_dataset-331"><span class="linenos">331</span></a>        <span class="nb">print</span><span class="p">(</span><span class="s2">&quot;Dataset:&quot;</span><span class="p">)</span>
</span><span id="view_dataset-332"><a href="#view_dataset-332"><span class="linenos">332</span></a>        <span class="nb">print</span><span class="p">(</span><span class="n">df</span><span class="p">)</span>
</span><span id="view_dataset-333"><a href="#view_dataset-333"><span class="linenos">333</span></a>    <span class="k">return</span> <span class="n">df</span>
</span></pre></div>


            <div class="docstring"><h1 id="view-dataset">View dataset</h1>

<p>View a dataset that exists on the twinLab cloud.</p>

<h2 id="arguments">Arguments</h2>

<ul>
<li><code>dataset_id</code>: <code>str</code>; name for the dataset when saved to the twinLab cloud</li>
<li><code>verbose</code>: <code>bool</code>, Optional, determining level of information returned to the user</li>
<li><code>debug</code>: <code>bool</code>, Optional, determining level of information logged on the server</li>
</ul>

<h2 id="returns">Returns</h2>

<ul>
<li><code>pandas.DataFrame</code> of the dataset.</li>
</ul>

<h2 id="example">Example</h2>

<div class="pdoc-code codehilite">
<pre><span></span><code><span class="kn">import</span> <span class="nn">pandas</span> <span class="k">as</span> <span class="nn">pd</span>
<span class="kn">import</span> <span class="nn">twinlab</span> <span class="k">as</span> <span class="nn">tl</span>

<span class="n">df</span> <span class="o">=</span> <span class="n">pd</span><span class="o">.</span><span class="n">DataFrame</span><span class="p">({</span><span class="s1">&#39;X&#39;</span><span class="p">:</span> <span class="p">[</span><span class="mi">1</span><span class="p">,</span> <span class="mi">2</span><span class="p">,</span> <span class="mi">3</span><span class="p">,</span> <span class="mi">4</span><span class="p">],</span> <span class="s1">&#39;y&#39;</span><span class="p">:</span> <span class="p">[</span><span class="mi">1</span><span class="p">,</span> <span class="mi">4</span><span class="p">,</span> <span class="mi">9</span><span class="p">,</span> <span class="mi">16</span><span class="p">]})</span>
<span class="n">tl</span><span class="o">.</span><span class="n">upload_dataset</span><span class="p">(</span><span class="n">df</span><span class="p">,</span> <span class="s2">&quot;my_dataset&quot;</span><span class="p">)</span>
<span class="n">df</span> <span class="o">=</span> <span class="n">tl</span><span class="o">.</span><span class="n">view_dataset</span><span class="p">(</span><span class="s2">&quot;my_dataset&quot;</span><span class="p">)</span>
<span class="nb">print</span><span class="p">(</span><span class="n">df</span><span class="p">)</span>
</code></pre>
</div>
</div>


                </section>
                <section id="query_dataset">
                            <input id="query_dataset-view-source" class="view-source-toggle-state" type="checkbox" aria-hidden="true" tabindex="-1">
<div class="attr function">
            
        <span class="def">def</span>
        <span class="name">query_dataset</span><span class="signature pdoc-code multiline">(<span class="param">	<span class="n">dataset_id</span><span class="p">:</span> <span class="nb">str</span>,</span><span class="param">	<span class="n">verbose</span><span class="p">:</span> <span class="n">Optional</span><span class="p">[</span><span class="nb">bool</span><span class="p">]</span> <span class="o">=</span> <span class="kc">False</span>,</span><span class="param">	<span class="n">debug</span><span class="p">:</span> <span class="n">Optional</span><span class="p">[</span><span class="nb">bool</span><span class="p">]</span> <span class="o">=</span> <span class="kc">False</span></span><span class="return-annotation">) -> <span class="n">pandas</span><span class="o">.</span><span class="n">core</span><span class="o">.</span><span class="n">frame</span><span class="o">.</span><span class="n">DataFrame</span>:</span></span>

                <label class="view-source-button" for="query_dataset-view-source"><span>View Source</span></label>

    </div>
    <a class="headerlink" href="#query_dataset"></a>
            <div class="pdoc-code codehilite"><pre><span></span><span id="query_dataset-337"><a href="#query_dataset-337"><span class="linenos">337</span></a><span class="k">def</span> <span class="nf">query_dataset</span><span class="p">(</span>
</span><span id="query_dataset-338"><a href="#query_dataset-338"><span class="linenos">338</span></a>    <span class="n">dataset_id</span><span class="p">:</span> <span class="nb">str</span><span class="p">,</span> <span class="n">verbose</span><span class="p">:</span> <span class="n">Optional</span><span class="p">[</span><span class="nb">bool</span><span class="p">]</span> <span class="o">=</span> <span class="kc">False</span><span class="p">,</span> <span class="n">debug</span><span class="p">:</span> <span class="n">Optional</span><span class="p">[</span><span class="nb">bool</span><span class="p">]</span> <span class="o">=</span> <span class="kc">False</span>
</span><span id="query_dataset-339"><a href="#query_dataset-339"><span class="linenos">339</span></a><span class="p">)</span> <span class="o">-&gt;</span> <span class="n">pd</span><span class="o">.</span><span class="n">DataFrame</span><span class="p">:</span>
</span><span id="query_dataset-340"><a href="#query_dataset-340"><span class="linenos">340</span></a><span class="w">    </span><span class="sd">&quot;&quot;&quot;</span>
</span><span id="query_dataset-341"><a href="#query_dataset-341"><span class="linenos">341</span></a><span class="sd">    # Query dataset</span>
</span><span id="query_dataset-342"><a href="#query_dataset-342"><span class="linenos">342</span></a>
</span><span id="query_dataset-343"><a href="#query_dataset-343"><span class="linenos">343</span></a><span class="sd">    Query a dataset that exists on the `twinLab` cloud by printing summary statistics.</span>
</span><span id="query_dataset-344"><a href="#query_dataset-344"><span class="linenos">344</span></a>
</span><span id="query_dataset-345"><a href="#query_dataset-345"><span class="linenos">345</span></a><span class="sd">    ## Arguments</span>
</span><span id="query_dataset-346"><a href="#query_dataset-346"><span class="linenos">346</span></a>
</span><span id="query_dataset-347"><a href="#query_dataset-347"><span class="linenos">347</span></a><span class="sd">    - `dataset_id`: `str`; name of dataset on S3 (same as the uploaded file name)</span>
</span><span id="query_dataset-348"><a href="#query_dataset-348"><span class="linenos">348</span></a><span class="sd">    - `verbose`: `bool`, Optional, determining level of information returned to the user</span>
</span><span id="query_dataset-349"><a href="#query_dataset-349"><span class="linenos">349</span></a><span class="sd">    - `debug`: `bool`, Optional, determining level of information logged on the server</span>
</span><span id="query_dataset-350"><a href="#query_dataset-350"><span class="linenos">350</span></a>
</span><span id="query_dataset-351"><a href="#query_dataset-351"><span class="linenos">351</span></a><span class="sd">    ## Returns</span>
</span><span id="query_dataset-352"><a href="#query_dataset-352"><span class="linenos">352</span></a>
</span><span id="query_dataset-353"><a href="#query_dataset-353"><span class="linenos">353</span></a><span class="sd">    - `pandas.DataFrame` containing summary statistics for the dataset.</span>
</span><span id="query_dataset-354"><a href="#query_dataset-354"><span class="linenos">354</span></a>
</span><span id="query_dataset-355"><a href="#query_dataset-355"><span class="linenos">355</span></a><span class="sd">    ## Example</span>
</span><span id="query_dataset-356"><a href="#query_dataset-356"><span class="linenos">356</span></a>
</span><span id="query_dataset-357"><a href="#query_dataset-357"><span class="linenos">357</span></a><span class="sd">    ```python</span>
</span><span id="query_dataset-358"><a href="#query_dataset-358"><span class="linenos">358</span></a><span class="sd">    import pandas as pd</span>
</span><span id="query_dataset-359"><a href="#query_dataset-359"><span class="linenos">359</span></a><span class="sd">    import twinlab as tl</span>
</span><span id="query_dataset-360"><a href="#query_dataset-360"><span class="linenos">360</span></a>
</span><span id="query_dataset-361"><a href="#query_dataset-361"><span class="linenos">361</span></a><span class="sd">    df = pd.DataFrame({&#39;X&#39;: [1, 2, 3, 4], &#39;y&#39;: [1, 4, 9, 16]})</span>
</span><span id="query_dataset-362"><a href="#query_dataset-362"><span class="linenos">362</span></a><span class="sd">    tl.upload_dataset(df, &quot;my_dataset&quot;)</span>
</span><span id="query_dataset-363"><a href="#query_dataset-363"><span class="linenos">363</span></a><span class="sd">    df = tl.query_dataset(&quot;my_dataset&quot;)</span>
</span><span id="query_dataset-364"><a href="#query_dataset-364"><span class="linenos">364</span></a><span class="sd">    print(df)</span>
</span><span id="query_dataset-365"><a href="#query_dataset-365"><span class="linenos">365</span></a><span class="sd">    ```</span>
</span><span id="query_dataset-366"><a href="#query_dataset-366"><span class="linenos">366</span></a><span class="sd">    &quot;&quot;&quot;</span>
</span><span id="query_dataset-367"><a href="#query_dataset-367"><span class="linenos">367</span></a>    <span class="n">response</span> <span class="o">=</span> <span class="n">api</span><span class="o">.</span><span class="n">summarise_dataset</span><span class="p">(</span><span class="n">dataset_id</span><span class="p">,</span> <span class="n">verbose</span><span class="o">=</span><span class="n">debug</span><span class="p">)</span>
</span><span id="query_dataset-368"><a href="#query_dataset-368"><span class="linenos">368</span></a>    <span class="n">csv_string</span> <span class="o">=</span> <span class="n">get_value_from_body</span><span class="p">(</span><span class="s2">&quot;dataset_summary&quot;</span><span class="p">,</span> <span class="n">response</span><span class="p">)</span>
</span><span id="query_dataset-369"><a href="#query_dataset-369"><span class="linenos">369</span></a>    <span class="n">csv_string</span> <span class="o">=</span> <span class="n">io</span><span class="o">.</span><span class="n">StringIO</span><span class="p">(</span><span class="n">csv_string</span><span class="p">)</span>
</span><span id="query_dataset-370"><a href="#query_dataset-370"><span class="linenos">370</span></a>    <span class="n">df</span> <span class="o">=</span> <span class="n">pd</span><span class="o">.</span><span class="n">read_csv</span><span class="p">(</span><span class="n">csv_string</span><span class="p">,</span> <span class="n">index_col</span><span class="o">=</span><span class="mi">0</span><span class="p">,</span> <span class="n">sep</span><span class="o">=</span><span class="s2">&quot;,&quot;</span><span class="p">)</span>
</span><span id="query_dataset-371"><a href="#query_dataset-371"><span class="linenos">371</span></a>    <span class="k">if</span> <span class="n">verbose</span><span class="p">:</span>
</span><span id="query_dataset-372"><a href="#query_dataset-372"><span class="linenos">372</span></a>        <span class="nb">print</span><span class="p">(</span><span class="s2">&quot;Dataset summary:&quot;</span><span class="p">)</span>
</span><span id="query_dataset-373"><a href="#query_dataset-373"><span class="linenos">373</span></a>        <span class="nb">print</span><span class="p">(</span><span class="n">df</span><span class="p">)</span>
</span><span id="query_dataset-374"><a href="#query_dataset-374"><span class="linenos">374</span></a>    <span class="k">return</span> <span class="n">df</span>
</span></pre></div>


            <div class="docstring"><h1 id="query-dataset">Query dataset</h1>

<p>Query a dataset that exists on the <code>twinLab</code> cloud by printing summary statistics.</p>

<h2 id="arguments">Arguments</h2>

<ul>
<li><code>dataset_id</code>: <code>str</code>; name of dataset on S3 (same as the uploaded file name)</li>
<li><code>verbose</code>: <code>bool</code>, Optional, determining level of information returned to the user</li>
<li><code>debug</code>: <code>bool</code>, Optional, determining level of information logged on the server</li>
</ul>

<h2 id="returns">Returns</h2>

<ul>
<li><code>pandas.DataFrame</code> containing summary statistics for the dataset.</li>
</ul>

<h2 id="example">Example</h2>

<div class="pdoc-code codehilite">
<pre><span></span><code><span class="kn">import</span> <span class="nn">pandas</span> <span class="k">as</span> <span class="nn">pd</span>
<span class="kn">import</span> <span class="nn">twinlab</span> <span class="k">as</span> <span class="nn">tl</span>

<span class="n">df</span> <span class="o">=</span> <span class="n">pd</span><span class="o">.</span><span class="n">DataFrame</span><span class="p">({</span><span class="s1">&#39;X&#39;</span><span class="p">:</span> <span class="p">[</span><span class="mi">1</span><span class="p">,</span> <span class="mi">2</span><span class="p">,</span> <span class="mi">3</span><span class="p">,</span> <span class="mi">4</span><span class="p">],</span> <span class="s1">&#39;y&#39;</span><span class="p">:</span> <span class="p">[</span><span class="mi">1</span><span class="p">,</span> <span class="mi">4</span><span class="p">,</span> <span class="mi">9</span><span class="p">,</span> <span class="mi">16</span><span class="p">]})</span>
<span class="n">tl</span><span class="o">.</span><span class="n">upload_dataset</span><span class="p">(</span><span class="n">df</span><span class="p">,</span> <span class="s2">&quot;my_dataset&quot;</span><span class="p">)</span>
<span class="n">df</span> <span class="o">=</span> <span class="n">tl</span><span class="o">.</span><span class="n">query_dataset</span><span class="p">(</span><span class="s2">&quot;my_dataset&quot;</span><span class="p">)</span>
<span class="nb">print</span><span class="p">(</span><span class="n">df</span><span class="p">)</span>
</code></pre>
</div>
</div>


                </section>
                <section id="delete_dataset">
                            <input id="delete_dataset-view-source" class="view-source-toggle-state" type="checkbox" aria-hidden="true" tabindex="-1">
<div class="attr function">
            
        <span class="def">def</span>
        <span class="name">delete_dataset</span><span class="signature pdoc-code multiline">(<span class="param">	<span class="n">dataset_id</span><span class="p">:</span> <span class="nb">str</span>,</span><span class="param">	<span class="n">verbose</span><span class="p">:</span> <span class="n">Optional</span><span class="p">[</span><span class="nb">bool</span><span class="p">]</span> <span class="o">=</span> <span class="kc">False</span>,</span><span class="param">	<span class="n">debug</span><span class="p">:</span> <span class="n">Optional</span><span class="p">[</span><span class="nb">bool</span><span class="p">]</span> <span class="o">=</span> <span class="kc">False</span></span><span class="return-annotation">) -> <span class="kc">None</span>:</span></span>

                <label class="view-source-button" for="delete_dataset-view-source"><span>View Source</span></label>

    </div>
    <a class="headerlink" href="#delete_dataset"></a>
            <div class="pdoc-code codehilite"><pre><span></span><span id="delete_dataset-378"><a href="#delete_dataset-378"><span class="linenos">378</span></a><span class="k">def</span> <span class="nf">delete_dataset</span><span class="p">(</span>
</span><span id="delete_dataset-379"><a href="#delete_dataset-379"><span class="linenos">379</span></a>    <span class="n">dataset_id</span><span class="p">:</span> <span class="nb">str</span><span class="p">,</span> <span class="n">verbose</span><span class="p">:</span> <span class="n">Optional</span><span class="p">[</span><span class="nb">bool</span><span class="p">]</span> <span class="o">=</span> <span class="kc">False</span><span class="p">,</span> <span class="n">debug</span><span class="p">:</span> <span class="n">Optional</span><span class="p">[</span><span class="nb">bool</span><span class="p">]</span> <span class="o">=</span> <span class="kc">False</span>
</span><span id="delete_dataset-380"><a href="#delete_dataset-380"><span class="linenos">380</span></a><span class="p">)</span> <span class="o">-&gt;</span> <span class="kc">None</span><span class="p">:</span>
</span><span id="delete_dataset-381"><a href="#delete_dataset-381"><span class="linenos">381</span></a><span class="w">    </span><span class="sd">&quot;&quot;&quot;</span>
</span><span id="delete_dataset-382"><a href="#delete_dataset-382"><span class="linenos">382</span></a><span class="sd">    # Delete dataset</span>
</span><span id="delete_dataset-383"><a href="#delete_dataset-383"><span class="linenos">383</span></a>
</span><span id="delete_dataset-384"><a href="#delete_dataset-384"><span class="linenos">384</span></a><span class="sd">    Delete a dataset from the `twinLab` cloud.</span>
</span><span id="delete_dataset-385"><a href="#delete_dataset-385"><span class="linenos">385</span></a>
</span><span id="delete_dataset-386"><a href="#delete_dataset-386"><span class="linenos">386</span></a><span class="sd">    ## Arguments</span>
</span><span id="delete_dataset-387"><a href="#delete_dataset-387"><span class="linenos">387</span></a>
</span><span id="delete_dataset-388"><a href="#delete_dataset-388"><span class="linenos">388</span></a><span class="sd">    - `dataset_id`: `str`; name of dataset to delete from the cloud</span>
</span><span id="delete_dataset-389"><a href="#delete_dataset-389"><span class="linenos">389</span></a><span class="sd">    - `verbose`: `bool`, Optional, determining level of information returned to the user</span>
</span><span id="delete_dataset-390"><a href="#delete_dataset-390"><span class="linenos">390</span></a><span class="sd">    - `debug`: `bool`, Optional, determining level of information logged on the server</span>
</span><span id="delete_dataset-391"><a href="#delete_dataset-391"><span class="linenos">391</span></a>
</span><span id="delete_dataset-392"><a href="#delete_dataset-392"><span class="linenos">392</span></a><span class="sd">    ## Example</span>
</span><span id="delete_dataset-393"><a href="#delete_dataset-393"><span class="linenos">393</span></a>
</span><span id="delete_dataset-394"><a href="#delete_dataset-394"><span class="linenos">394</span></a><span class="sd">    ```python</span>
</span><span id="delete_dataset-395"><a href="#delete_dataset-395"><span class="linenos">395</span></a><span class="sd">    import pandas as pd</span>
</span><span id="delete_dataset-396"><a href="#delete_dataset-396"><span class="linenos">396</span></a><span class="sd">    import twinlab as tl</span>
</span><span id="delete_dataset-397"><a href="#delete_dataset-397"><span class="linenos">397</span></a>
</span><span id="delete_dataset-398"><a href="#delete_dataset-398"><span class="linenos">398</span></a><span class="sd">    df = pd.DataFrame({&#39;X&#39;: [1, 2, 3, 4], &#39;y&#39;: [1, 4, 9, 16]})</span>
</span><span id="delete_dataset-399"><a href="#delete_dataset-399"><span class="linenos">399</span></a><span class="sd">    tl.upload_dataset(df, &quot;my_dataset&quot;)</span>
</span><span id="delete_dataset-400"><a href="#delete_dataset-400"><span class="linenos">400</span></a><span class="sd">    tl.delete_dataset(&quot;my_dataset&quot;)</span>
</span><span id="delete_dataset-401"><a href="#delete_dataset-401"><span class="linenos">401</span></a><span class="sd">    ```</span>
</span><span id="delete_dataset-402"><a href="#delete_dataset-402"><span class="linenos">402</span></a><span class="sd">    &quot;&quot;&quot;</span>
</span><span id="delete_dataset-403"><a href="#delete_dataset-403"><span class="linenos">403</span></a>    <span class="n">response</span> <span class="o">=</span> <span class="n">api</span><span class="o">.</span><span class="n">delete_dataset</span><span class="p">(</span><span class="n">dataset_id</span><span class="p">,</span> <span class="n">verbose</span><span class="o">=</span><span class="n">debug</span><span class="p">)</span>
</span><span id="delete_dataset-404"><a href="#delete_dataset-404"><span class="linenos">404</span></a>    <span class="k">if</span> <span class="n">verbose</span><span class="p">:</span>
</span><span id="delete_dataset-405"><a href="#delete_dataset-405"><span class="linenos">405</span></a>        <span class="n">message</span> <span class="o">=</span> <span class="n">_get_message</span><span class="p">(</span><span class="n">response</span><span class="p">)</span>
</span><span id="delete_dataset-406"><a href="#delete_dataset-406"><span class="linenos">406</span></a>        <span class="nb">print</span><span class="p">(</span><span class="n">message</span><span class="p">)</span>
</span></pre></div>


            <div class="docstring"><h1 id="delete-dataset">Delete dataset</h1>

<p>Delete a dataset from the <code>twinLab</code> cloud.</p>

<h2 id="arguments">Arguments</h2>

<ul>
<li><code>dataset_id</code>: <code>str</code>; name of dataset to delete from the cloud</li>
<li><code>verbose</code>: <code>bool</code>, Optional, determining level of information returned to the user</li>
<li><code>debug</code>: <code>bool</code>, Optional, determining level of information logged on the server</li>
</ul>

<h2 id="example">Example</h2>

<div class="pdoc-code codehilite">
<pre><span></span><code><span class="kn">import</span> <span class="nn">pandas</span> <span class="k">as</span> <span class="nn">pd</span>
<span class="kn">import</span> <span class="nn">twinlab</span> <span class="k">as</span> <span class="nn">tl</span>

<span class="n">df</span> <span class="o">=</span> <span class="n">pd</span><span class="o">.</span><span class="n">DataFrame</span><span class="p">({</span><span class="s1">&#39;X&#39;</span><span class="p">:</span> <span class="p">[</span><span class="mi">1</span><span class="p">,</span> <span class="mi">2</span><span class="p">,</span> <span class="mi">3</span><span class="p">,</span> <span class="mi">4</span><span class="p">],</span> <span class="s1">&#39;y&#39;</span><span class="p">:</span> <span class="p">[</span><span class="mi">1</span><span class="p">,</span> <span class="mi">4</span><span class="p">,</span> <span class="mi">9</span><span class="p">,</span> <span class="mi">16</span><span class="p">]})</span>
<span class="n">tl</span><span class="o">.</span><span class="n">upload_dataset</span><span class="p">(</span><span class="n">df</span><span class="p">,</span> <span class="s2">&quot;my_dataset&quot;</span><span class="p">)</span>
<span class="n">tl</span><span class="o">.</span><span class="n">delete_dataset</span><span class="p">(</span><span class="s2">&quot;my_dataset&quot;</span><span class="p">)</span>
</code></pre>
</div>
</div>


                </section>
                <section id="train_campaign">
                            <input id="train_campaign-view-source" class="view-source-toggle-state" type="checkbox" aria-hidden="true" tabindex="-1">
<div class="attr function">
            
        <span class="def">def</span>
        <span class="name">train_campaign</span><span class="signature pdoc-code multiline">(<span class="param">	<span class="n">filepath_or_params</span><span class="p">:</span> <span class="n">Union</span><span class="p">[</span><span class="nb">str</span><span class="p">,</span> <span class="nb">dict</span><span class="p">]</span>,</span><span class="param">	<span class="n">campaign_id</span><span class="p">:</span> <span class="nb">str</span>,</span><span class="param">	<span class="n">ping_time</span><span class="p">:</span> <span class="n">Optional</span><span class="p">[</span><span class="nb">float</span><span class="p">]</span> <span class="o">=</span> <span class="mf">1.0</span>,</span><span class="param">	<span class="n">processor</span><span class="p">:</span> <span class="n">Optional</span><span class="p">[</span><span class="nb">str</span><span class="p">]</span> <span class="o">=</span> <span class="s1">&#39;cpu&#39;</span>,</span><span class="param">	<span class="n">verbose</span><span class="p">:</span> <span class="n">Optional</span><span class="p">[</span><span class="nb">bool</span><span class="p">]</span> <span class="o">=</span> <span class="kc">False</span>,</span><span class="param">	<span class="n">debug</span><span class="p">:</span> <span class="n">Optional</span><span class="p">[</span><span class="nb">bool</span><span class="p">]</span> <span class="o">=</span> <span class="kc">False</span></span><span class="return-annotation">) -> <span class="kc">None</span>:</span></span>

                <label class="view-source-button" for="train_campaign-view-source"><span>View Source</span></label>

    </div>
    <a class="headerlink" href="#train_campaign"></a>
            <div class="pdoc-code codehilite"><pre><span></span><span id="train_campaign-415"><a href="#train_campaign-415"><span class="linenos">415</span></a><span class="k">def</span> <span class="nf">train_campaign</span><span class="p">(</span>
</span><span id="train_campaign-416"><a href="#train_campaign-416"><span class="linenos">416</span></a>    <span class="n">filepath_or_params</span><span class="p">:</span> <span class="n">Union</span><span class="p">[</span><span class="nb">str</span><span class="p">,</span> <span class="nb">dict</span><span class="p">],</span>
</span><span id="train_campaign-417"><a href="#train_campaign-417"><span class="linenos">417</span></a>    <span class="n">campaign_id</span><span class="p">:</span> <span class="nb">str</span><span class="p">,</span>
</span><span id="train_campaign-418"><a href="#train_campaign-418"><span class="linenos">418</span></a>    <span class="n">ping_time</span><span class="p">:</span> <span class="n">Optional</span><span class="p">[</span><span class="nb">float</span><span class="p">]</span> <span class="o">=</span> <span class="mf">1.0</span><span class="p">,</span>
</span><span id="train_campaign-419"><a href="#train_campaign-419"><span class="linenos">419</span></a>    <span class="n">processor</span><span class="p">:</span> <span class="n">Optional</span><span class="p">[</span><span class="nb">str</span><span class="p">]</span> <span class="o">=</span> <span class="s2">&quot;cpu&quot;</span><span class="p">,</span>
</span><span id="train_campaign-420"><a href="#train_campaign-420"><span class="linenos">420</span></a>    <span class="n">verbose</span><span class="p">:</span> <span class="n">Optional</span><span class="p">[</span><span class="nb">bool</span><span class="p">]</span> <span class="o">=</span> <span class="kc">False</span><span class="p">,</span>
</span><span id="train_campaign-421"><a href="#train_campaign-421"><span class="linenos">421</span></a>    <span class="n">debug</span><span class="p">:</span> <span class="n">Optional</span><span class="p">[</span><span class="nb">bool</span><span class="p">]</span> <span class="o">=</span> <span class="kc">False</span><span class="p">,</span>
</span><span id="train_campaign-422"><a href="#train_campaign-422"><span class="linenos">422</span></a><span class="p">)</span> <span class="o">-&gt;</span> <span class="kc">None</span><span class="p">:</span>
</span><span id="train_campaign-423"><a href="#train_campaign-423"><span class="linenos">423</span></a><span class="w">    </span><span class="sd">&quot;&quot;&quot;</span>
</span><span id="train_campaign-424"><a href="#train_campaign-424"><span class="linenos">424</span></a><span class="sd">    # Train campaign</span>
</span><span id="train_campaign-425"><a href="#train_campaign-425"><span class="linenos">425</span></a>
</span><span id="train_campaign-426"><a href="#train_campaign-426"><span class="linenos">426</span></a><span class="sd">    Train a campaign in the `twinLab` cloud.</span>
</span><span id="train_campaign-427"><a href="#train_campaign-427"><span class="linenos">427</span></a>
</span><span id="train_campaign-428"><a href="#train_campaign-428"><span class="linenos">428</span></a><span class="sd">    ## Arguments</span>
</span><span id="train_campaign-429"><a href="#train_campaign-429"><span class="linenos">429</span></a>
</span><span id="train_campaign-430"><a href="#train_campaign-430"><span class="linenos">430</span></a><span class="sd">    - `filepath_or_params`: `str`, `dict`, Union; filepath to local json or parameters dictionary for training</span>
</span><span id="train_campaign-431"><a href="#train_campaign-431"><span class="linenos">431</span></a><span class="sd">    - `campaign_id`: `str`, name for the final trained campaign</span>
</span><span id="train_campaign-432"><a href="#train_campaign-432"><span class="linenos">432</span></a><span class="sd">    **Warning:** If the `campaign_id` already exists for the current cloud account, it will be overwritten by the</span>
</span><span id="train_campaign-433"><a href="#train_campaign-433"><span class="linenos">433</span></a><span class="sd">    newly trained campaign</span>
</span><span id="train_campaign-434"><a href="#train_campaign-434"><span class="linenos">434</span></a><span class="sd">    - `ping_time`: `float`, Optional, time between pings to the server to check if the job is complete [s]</span>
</span><span id="train_campaign-435"><a href="#train_campaign-435"><span class="linenos">435</span></a><span class="sd">    - `processor`: `str`, Optional, processor to use for sampling (&quot;cpu&quot;; &quot;gpu&quot;)</span>
</span><span id="train_campaign-436"><a href="#train_campaign-436"><span class="linenos">436</span></a><span class="sd">    - `verbose`: `bool`, Optional, determining level of information returned to the user</span>
</span><span id="train_campaign-437"><a href="#train_campaign-437"><span class="linenos">437</span></a><span class="sd">    - `debug`: `bool`, Optional, determining level of information logged on the server</span>
</span><span id="train_campaign-438"><a href="#train_campaign-438"><span class="linenos">438</span></a>
</span><span id="train_campaign-439"><a href="#train_campaign-439"><span class="linenos">439</span></a><span class="sd">    The parameters retrieved from the first argument are divided into 2 different sets of parameters, one for</span>
</span><span id="train_campaign-440"><a href="#train_campaign-440"><span class="linenos">440</span></a><span class="sd">    setting up the campaign and the other for training the campaign.</span>
</span><span id="train_campaign-441"><a href="#train_campaign-441"><span class="linenos">441</span></a>
</span><span id="train_campaign-442"><a href="#train_campaign-442"><span class="linenos">442</span></a><span class="sd">    Parameters to setup the campaign(used during initialization of a Campaign class object):</span>
</span><span id="train_campaign-443"><a href="#train_campaign-443"><span class="linenos">443</span></a><span class="sd">    - `dataset_id`: `str`, dataset_id of the dataset as stored in the cloud</span>
</span><span id="train_campaign-444"><a href="#train_campaign-444"><span class="linenos">444</span></a><span class="sd">    - `inputs`: `list`, a list of strings referring to the columns in the</span>
</span><span id="train_campaign-445"><a href="#train_campaign-445"><span class="linenos">445</span></a><span class="sd">                Pandas DataFrame that will be used as input parameters</span>
</span><span id="train_campaign-446"><a href="#train_campaign-446"><span class="linenos">446</span></a><span class="sd">    - `outputs`: `list`, a list of strings referring to the columns in the</span>
</span><span id="train_campaign-447"><a href="#train_campaign-447"><span class="linenos">447</span></a><span class="sd">                Pandas DataFrame that will be used as output parameters</span>
</span><span id="train_campaign-448"><a href="#train_campaign-448"><span class="linenos">448</span></a><span class="sd">    - `estimator`: `str`, Optional, The type of estimator used in the pipeline</span>
</span><span id="train_campaign-449"><a href="#train_campaign-449"><span class="linenos">449</span></a><span class="sd">                (&quot;gaussian_process_regression&quot; or &quot;gradient_boosting_regression&quot;)</span>
</span><span id="train_campaign-450"><a href="#train_campaign-450"><span class="linenos">450</span></a><span class="sd">    - `estimator_kwargs`: `dict`, Optional, keywords passed to the underlying estimator</span>
</span><span id="train_campaign-451"><a href="#train_campaign-451"><span class="linenos">451</span></a><span class="sd">                The estimator_kwargs dictionary for &quot;gaussian_process_regression&quot; allows the</span>
</span><span id="train_campaign-452"><a href="#train_campaign-452"><span class="linenos">452</span></a><span class="sd">                following keywords:</span>
</span><span id="train_campaign-453"><a href="#train_campaign-453"><span class="linenos">453</span></a><span class="sd">                `detrend`: `bool`, Optional, specifies whther to linear detrend the output</span>
</span><span id="train_campaign-454"><a href="#train_campaign-454"><span class="linenos">454</span></a><span class="sd">                        data before estimator fitting, default is False</span>
</span><span id="train_campaign-455"><a href="#train_campaign-455"><span class="linenos">455</span></a><span class="sd">                `device`: `str`, Optional, specifies whether to fit the estimator using</span>
</span><span id="train_campaign-456"><a href="#train_campaign-456"><span class="linenos">456</span></a><span class="sd">                        &quot;cpu&quot; or &quot;gpu&quot;, default is &quot;cpu&quot;</span>
</span><span id="train_campaign-457"><a href="#train_campaign-457"><span class="linenos">457</span></a><span class="sd">    - `decompose_input`: `bool`, Optional, specifies whether the input parameters</span>
</span><span id="train_campaign-458"><a href="#train_campaign-458"><span class="linenos">458</span></a><span class="sd">                should be decomposed</span>
</span><span id="train_campaign-459"><a href="#train_campaign-459"><span class="linenos">459</span></a><span class="sd">    - `input_explained_variance`: `float`, Optional, specifies how much of the</span>
</span><span id="train_campaign-460"><a href="#train_campaign-460"><span class="linenos">460</span></a><span class="sd">                variance should be explained after the truncation of the SVD</span>
</span><span id="train_campaign-461"><a href="#train_campaign-461"><span class="linenos">461</span></a><span class="sd">                (Singular Value Decomposition) for functional input</span>
</span><span id="train_campaign-462"><a href="#train_campaign-462"><span class="linenos">462</span></a><span class="sd">    - `decompose_output`: `bool`, Optional, specifies whether the output parameters</span>
</span><span id="train_campaign-463"><a href="#train_campaign-463"><span class="linenos">463</span></a><span class="sd">                should be decomposed</span>
</span><span id="train_campaign-464"><a href="#train_campaign-464"><span class="linenos">464</span></a><span class="sd">    - `output_explained_variance`: `float`, Optional, specifies how much of the</span>
</span><span id="train_campaign-465"><a href="#train_campaign-465"><span class="linenos">465</span></a><span class="sd">                variance should be explained after the truncation of the SVD</span>
</span><span id="train_campaign-466"><a href="#train_campaign-466"><span class="linenos">466</span></a><span class="sd">                (Singular Value Decomposition) for functional output</span>
</span><span id="train_campaign-467"><a href="#train_campaign-467"><span class="linenos">467</span></a>
</span><span id="train_campaign-468"><a href="#train_campaign-468"><span class="linenos">468</span></a><span class="sd">    Parameters to train the campaign(used when fit() function is called using a Campaign class object for training):</span>
</span><span id="train_campaign-469"><a href="#train_campaign-469"><span class="linenos">469</span></a><span class="sd">    - `train_test_ratio`: `float`, Optional, specifies the ratio of training samples in</span>
</span><span id="train_campaign-470"><a href="#train_campaign-470"><span class="linenos">470</span></a><span class="sd">            the dataset</span>
</span><span id="train_campaign-471"><a href="#train_campaign-471"><span class="linenos">471</span></a><span class="sd">    - `model_selection`: `bool`, Optional, whether to run model selection</span>
</span><span id="train_campaign-472"><a href="#train_campaign-472"><span class="linenos">472</span></a><span class="sd">    - `model_selection_kwargs`: `dict`, Optional, keywords passed to the model</span>
</span><span id="train_campaign-473"><a href="#train_campaign-473"><span class="linenos">473</span></a><span class="sd">            selection process</span>
</span><span id="train_campaign-474"><a href="#train_campaign-474"><span class="linenos">474</span></a><span class="sd">            The model_selection_kwargs dictionary for &quot;gaussian_process_regression&quot; allows the</span>
</span><span id="train_campaign-475"><a href="#train_campaign-475"><span class="linenos">475</span></a><span class="sd">            following keywords:</span>
</span><span id="train_campaign-476"><a href="#train_campaign-476"><span class="linenos">476</span></a><span class="sd">            `seed`: `int`, Optional, specifies the seed for the random number genrator for every</span>
</span><span id="train_campaign-477"><a href="#train_campaign-477"><span class="linenos">477</span></a><span class="sd">                trial of the model selection process</span>
</span><span id="train_campaign-478"><a href="#train_campaign-478"><span class="linenos">478</span></a><span class="sd">            `evaluation_metric`: `str`, Optional, specifies the evaluation metric used to score</span>
</span><span id="train_campaign-479"><a href="#train_campaign-479"><span class="linenos">479</span></a><span class="sd">                different configuration during the model selection process, can be &quot;BIC&quot; or &quot;MSLL&quot;,</span>
</span><span id="train_campaign-480"><a href="#train_campaign-480"><span class="linenos">480</span></a><span class="sd">                default is &quot;MSLL&quot;</span>
</span><span id="train_campaign-481"><a href="#train_campaign-481"><span class="linenos">481</span></a><span class="sd">            `val_ratio`: `float`, Optional, specifies the percentage of random validation data</span>
</span><span id="train_campaign-482"><a href="#train_campaign-482"><span class="linenos">482</span></a><span class="sd">                allocated to to compute the &quot;BIC&quot; metric, default is 0.2</span>
</span><span id="train_campaign-483"><a href="#train_campaign-483"><span class="linenos">483</span></a><span class="sd">            `base_kernels`: Set[str], Optional, specifies the list of kernels to use for</span>
</span><span id="train_campaign-484"><a href="#train_campaign-484"><span class="linenos">484</span></a><span class="sd">                Compositional Kernel Search, can be &quot;all&quot;, &quot;restricted&quot; or Set[str] object</span>
</span><span id="train_campaign-485"><a href="#train_campaign-485"><span class="linenos">485</span></a><span class="sd">                Set of available kernels are [&quot;LIN&quot;, &quot;M12&quot;, &quot;M32&quot;, &quot;M52&quot;, &quot;PER&quot;, &quot;RBF&quot;, &quot;RQF&quot;],</span>
</span><span id="train_campaign-486"><a href="#train_campaign-486"><span class="linenos">486</span></a><span class="sd">                default is &quot;restricted&quot; and uses [&quot;LIN&quot;, &quot;M32&quot;, &quot;M52&quot;, &quot;PER&quot;, &quot;RBF&quot;]</span>
</span><span id="train_campaign-487"><a href="#train_campaign-487"><span class="linenos">487</span></a><span class="sd">            `depth`: `int`, Optional, specifies the number of base kernels to be combined in</span>
</span><span id="train_campaign-488"><a href="#train_campaign-488"><span class="linenos">488</span></a><span class="sd">                the Compositional Kernel Search, depth=3 means the resulting kernel may be</span>
</span><span id="train_campaign-489"><a href="#train_campaign-489"><span class="linenos">489</span></a><span class="sd">                composed from three base kernels, e.g. &quot;(LIN+PER)*RBF&quot; or &quot;(M12*RBF)+RQF&quot;,</span>
</span><span id="train_campaign-490"><a href="#train_campaign-490"><span class="linenos">490</span></a><span class="sd">                default is 1</span>
</span><span id="train_campaign-491"><a href="#train_campaign-491"><span class="linenos">491</span></a><span class="sd">            `beam`: `int`, Optional, specifies the beam width of the Compositional Kernel Search</span>
</span><span id="train_campaign-492"><a href="#train_campaign-492"><span class="linenos">492</span></a><span class="sd">                algorithm, beam=1 is greedy search, beam=None performs breadth-first search and</span>
</span><span id="train_campaign-493"><a href="#train_campaign-493"><span class="linenos">493</span></a><span class="sd">                beam&gt;1 perfroms beam search with the specified beam value, default is None</span>
</span><span id="train_campaign-494"><a href="#train_campaign-494"><span class="linenos">494</span></a><span class="sd">            `resources_per_trial`: `dict`, Optional, The amount of CPU and GPU resources allocated</span>
</span><span id="train_campaign-495"><a href="#train_campaign-495"><span class="linenos">495</span></a><span class="sd">                to each trial of model selection, default is {&quot;cpu&quot;: 1, &quot;gpu&quot;: 0}</span>
</span><span id="train_campaign-496"><a href="#train_campaign-496"><span class="linenos">496</span></a><span class="sd">    - `seed`: `int`, Optional, specifies the seed for the random number generator</span>
</span><span id="train_campaign-497"><a href="#train_campaign-497"><span class="linenos">497</span></a>
</span><span id="train_campaign-498"><a href="#train_campaign-498"><span class="linenos">498</span></a><span class="sd">    ## Example</span>
</span><span id="train_campaign-499"><a href="#train_campaign-499"><span class="linenos">499</span></a>
</span><span id="train_campaign-500"><a href="#train_campaign-500"><span class="linenos">500</span></a><span class="sd">    Train using a local `json` parameters file:</span>
</span><span id="train_campaign-501"><a href="#train_campaign-501"><span class="linenos">501</span></a>
</span><span id="train_campaign-502"><a href="#train_campaign-502"><span class="linenos">502</span></a><span class="sd">    ```python</span>
</span><span id="train_campaign-503"><a href="#train_campaign-503"><span class="linenos">503</span></a><span class="sd">    import twinlab as tl</span>
</span><span id="train_campaign-504"><a href="#train_campaign-504"><span class="linenos">504</span></a>
</span><span id="train_campaign-505"><a href="#train_campaign-505"><span class="linenos">505</span></a><span class="sd">    tl.train_campaign(&quot;path/to/params.json&quot;, &quot;my_campaign&quot;)</span>
</span><span id="train_campaign-506"><a href="#train_campaign-506"><span class="linenos">506</span></a><span class="sd">    ```</span>
</span><span id="train_campaign-507"><a href="#train_campaign-507"><span class="linenos">507</span></a>
</span><span id="train_campaign-508"><a href="#train_campaign-508"><span class="linenos">508</span></a><span class="sd">    Train via a `python` dictionary:</span>
</span><span id="train_campaign-509"><a href="#train_campaign-509"><span class="linenos">509</span></a>
</span><span id="train_campaign-510"><a href="#train_campaign-510"><span class="linenos">510</span></a><span class="sd">    ```python</span>
</span><span id="train_campaign-511"><a href="#train_campaign-511"><span class="linenos">511</span></a><span class="sd">    import pandas as pd</span>
</span><span id="train_campaign-512"><a href="#train_campaign-512"><span class="linenos">512</span></a><span class="sd">    import twinlab as tl</span>
</span><span id="train_campaign-513"><a href="#train_campaign-513"><span class="linenos">513</span></a>
</span><span id="train_campaign-514"><a href="#train_campaign-514"><span class="linenos">514</span></a><span class="sd">    df = pd.DataFrame({&#39;X&#39;: [1, 2, 3, 4], &#39;y&#39;: [1, 4, 9, 16]})</span>
</span><span id="train_campaign-515"><a href="#train_campaign-515"><span class="linenos">515</span></a><span class="sd">    tl.upload_dataset(df, &quot;my_dataset&quot;)</span>
</span><span id="train_campaign-516"><a href="#train_campaign-516"><span class="linenos">516</span></a><span class="sd">    params = {</span>
</span><span id="train_campaign-517"><a href="#train_campaign-517"><span class="linenos">517</span></a><span class="sd">        &quot;dataset_id&quot;: &quot;my_dataset&quot;,</span>
</span><span id="train_campaign-518"><a href="#train_campaign-518"><span class="linenos">518</span></a><span class="sd">        &quot;inputs&quot;: [&quot;X&quot;],</span>
</span><span id="train_campaign-519"><a href="#train_campaign-519"><span class="linenos">519</span></a><span class="sd">        &quot;outputs&quot;: [&quot;y&quot;],</span>
</span><span id="train_campaign-520"><a href="#train_campaign-520"><span class="linenos">520</span></a><span class="sd">    }</span>
</span><span id="train_campaign-521"><a href="#train_campaign-521"><span class="linenos">521</span></a><span class="sd">    tl.train_campaign(params, &quot;my_campaign&quot;)</span>
</span><span id="train_campaign-522"><a href="#train_campaign-522"><span class="linenos">522</span></a><span class="sd">    ```</span>
</span><span id="train_campaign-523"><a href="#train_campaign-523"><span class="linenos">523</span></a><span class="sd">    &quot;&quot;&quot;</span>
</span><span id="train_campaign-524"><a href="#train_campaign-524"><span class="linenos">524</span></a>    <span class="k">if</span> <span class="nb">type</span><span class="p">(</span><span class="n">filepath_or_params</span><span class="p">)</span> <span class="ow">is</span> <span class="nb">dict</span><span class="p">:</span>
</span><span id="train_campaign-525"><a href="#train_campaign-525"><span class="linenos">525</span></a>        <span class="n">params</span> <span class="o">=</span> <span class="n">filepath_or_params</span>
</span><span id="train_campaign-526"><a href="#train_campaign-526"><span class="linenos">526</span></a>    <span class="k">elif</span> <span class="nb">type</span><span class="p">(</span><span class="n">filepath_or_params</span><span class="p">)</span> <span class="ow">is</span> <span class="nb">str</span><span class="p">:</span>
</span><span id="train_campaign-527"><a href="#train_campaign-527"><span class="linenos">527</span></a>        <span class="n">filepath</span> <span class="o">=</span> <span class="n">filepath_or_params</span>
</span><span id="train_campaign-528"><a href="#train_campaign-528"><span class="linenos">528</span></a>        <span class="n">params</span> <span class="o">=</span> <span class="n">json</span><span class="o">.</span><span class="n">load</span><span class="p">(</span><span class="nb">open</span><span class="p">(</span><span class="n">filepath</span><span class="p">))</span>
</span><span id="train_campaign-529"><a href="#train_campaign-529"><span class="linenos">529</span></a>    <span class="k">else</span><span class="p">:</span>
</span><span id="train_campaign-530"><a href="#train_campaign-530"><span class="linenos">530</span></a>        <span class="nb">print</span><span class="p">(</span><span class="s2">&quot;Type:&quot;</span><span class="p">,</span> <span class="nb">type</span><span class="p">(</span><span class="n">filepath_or_params</span><span class="p">))</span>
</span><span id="train_campaign-531"><a href="#train_campaign-531"><span class="linenos">531</span></a>        <span class="k">raise</span> <span class="ne">ValueError</span><span class="p">(</span><span class="s2">&quot;filepath_or_params must be either a string or a dictionary&quot;</span><span class="p">)</span>
</span><span id="train_campaign-532"><a href="#train_campaign-532"><span class="linenos">532</span></a>    <span class="n">params</span> <span class="o">=</span> <span class="n">utils</span><span class="o">.</span><span class="n">coerce_params_dict</span><span class="p">(</span><span class="n">params</span><span class="p">)</span>
</span><span id="train_campaign-533"><a href="#train_campaign-533"><span class="linenos">533</span></a>    <span class="n">params_str</span> <span class="o">=</span> <span class="n">json</span><span class="o">.</span><span class="n">dumps</span><span class="p">(</span><span class="n">params</span><span class="p">)</span>
</span><span id="train_campaign-534"><a href="#train_campaign-534"><span class="linenos">534</span></a>    <span class="n">response</span> <span class="o">=</span> <span class="n">api</span><span class="o">.</span><span class="n">train_model</span><span class="p">(</span>
</span><span id="train_campaign-535"><a href="#train_campaign-535"><span class="linenos">535</span></a>        <span class="n">campaign_id</span><span class="p">,</span> <span class="n">params_str</span><span class="p">,</span> <span class="n">processor</span><span class="o">=</span><span class="n">processor</span><span class="p">,</span> <span class="n">verbose</span><span class="o">=</span><span class="n">debug</span>
</span><span id="train_campaign-536"><a href="#train_campaign-536"><span class="linenos">536</span></a>    <span class="p">)</span>
</span><span id="train_campaign-537"><a href="#train_campaign-537"><span class="linenos">537</span></a>    <span class="k">if</span> <span class="n">verbose</span><span class="p">:</span>
</span><span id="train_campaign-538"><a href="#train_campaign-538"><span class="linenos">538</span></a>        <span class="n">message</span> <span class="o">=</span> <span class="n">_get_message</span><span class="p">(</span><span class="n">response</span><span class="p">)</span>
</span><span id="train_campaign-539"><a href="#train_campaign-539"><span class="linenos">539</span></a>        <span class="nb">print</span><span class="p">(</span><span class="n">message</span><span class="p">)</span>
</span><span id="train_campaign-540"><a href="#train_campaign-540"><span class="linenos">540</span></a>
</span><span id="train_campaign-541"><a href="#train_campaign-541"><span class="linenos">541</span></a>    <span class="c1"># Wait for job to complete</span>
</span><span id="train_campaign-542"><a href="#train_campaign-542"><span class="linenos">542</span></a>    <span class="n">complete</span> <span class="o">=</span> <span class="kc">False</span>
</span><span id="train_campaign-543"><a href="#train_campaign-543"><span class="linenos">543</span></a>    <span class="k">while</span> <span class="ow">not</span> <span class="n">complete</span><span class="p">:</span>
</span><span id="train_campaign-544"><a href="#train_campaign-544"><span class="linenos">544</span></a>        <span class="n">status</span> <span class="o">=</span> <span class="n">_status_campaign</span><span class="p">(</span><span class="n">campaign_id</span><span class="p">,</span> <span class="n">verbose</span><span class="o">=</span><span class="kc">False</span><span class="p">,</span> <span class="n">debug</span><span class="o">=</span><span class="n">debug</span><span class="p">)</span>
</span><span id="train_campaign-545"><a href="#train_campaign-545"><span class="linenos">545</span></a>        <span class="n">complete</span> <span class="o">=</span> <span class="n">get_value_from_body</span><span class="p">(</span><span class="s2">&quot;job_complete&quot;</span><span class="p">,</span> <span class="n">status</span><span class="p">)</span>
</span><span id="train_campaign-546"><a href="#train_campaign-546"><span class="linenos">546</span></a>        <span class="n">time</span><span class="o">.</span><span class="n">sleep</span><span class="p">(</span><span class="n">ping_time</span><span class="p">)</span>
</span></pre></div>


            <div class="docstring"><h1 id="train-campaign">Train campaign</h1>

<p>Train a campaign in the <code>twinLab</code> cloud.</p>

<h2 id="arguments">Arguments</h2>

<ul>
<li><code>filepath_or_params</code>: <code>str</code>, <code>dict</code>, Union; filepath to local json or parameters dictionary for training</li>
<li><code>campaign_id</code>: <code>str</code>, name for the final trained campaign
<strong>Warning:</strong> If the <code>campaign_id</code> already exists for the current cloud account, it will be overwritten by the
newly trained campaign</li>
<li><code>ping_time</code>: <code>float</code>, Optional, time between pings to the server to check if the job is complete [s]</li>
<li><code>processor</code>: <code>str</code>, Optional, processor to use for sampling ("cpu"; "gpu")</li>
<li><code>verbose</code>: <code>bool</code>, Optional, determining level of information returned to the user</li>
<li><code>debug</code>: <code>bool</code>, Optional, determining level of information logged on the server</li>
</ul>

<p>The parameters retrieved from the first argument are divided into 2 different sets of parameters, one for
setting up the campaign and the other for training the campaign.</p>

<p>Parameters to setup the campaign(used during initialization of a Campaign class object):</p>

<ul>
<li><code>dataset_id</code>: <code>str</code>, dataset_id of the dataset as stored in the cloud</li>
<li><code>inputs</code>: <code>list</code>, a list of strings referring to the columns in the
Pandas DataFrame that will be used as input parameters</li>
<li><code>outputs</code>: <code>list</code>, a list of strings referring to the columns in the
Pandas DataFrame that will be used as output parameters</li>
<li><code>estimator</code>: <code>str</code>, Optional, The type of estimator used in the pipeline
("gaussian_process_regression" or "gradient_boosting_regression")</li>
<li><code>estimator_kwargs</code>: <code>dict</code>, Optional, keywords passed to the underlying estimator
The estimator_kwargs dictionary for "gaussian_process_regression" allows the
following keywords:
<code>detrend</code>: <code>bool</code>, Optional, specifies whther to linear detrend the output
        data before estimator fitting, default is False
<code>device</code>: <code>str</code>, Optional, specifies whether to fit the estimator using
        "cpu" or "gpu", default is "cpu"</li>
<li><code>decompose_input</code>: <code>bool</code>, Optional, specifies whether the input parameters
should be decomposed</li>
<li><code>input_explained_variance</code>: <code>float</code>, Optional, specifies how much of the
variance should be explained after the truncation of the SVD
(Singular Value Decomposition) for functional input</li>
<li><code>decompose_output</code>: <code>bool</code>, Optional, specifies whether the output parameters
should be decomposed</li>
<li><code>output_explained_variance</code>: <code>float</code>, Optional, specifies how much of the
variance should be explained after the truncation of the SVD
(Singular Value Decomposition) for functional output</li>
</ul>

<p>Parameters to train the campaign(used when fit() function is called using a Campaign class object for training):</p>

<ul>
<li><code>train_test_ratio</code>: <code>float</code>, Optional, specifies the ratio of training samples in
the dataset</li>
<li><code>model_selection</code>: <code>bool</code>, Optional, whether to run model selection</li>
<li><code>model_selection_kwargs</code>: <code>dict</code>, Optional, keywords passed to the model
selection process
The model_selection_kwargs dictionary for "gaussian_process_regression" allows the
following keywords:
<code>seed</code>: <code>int</code>, Optional, specifies the seed for the random number genrator for every
    trial of the model selection process
<code>evaluation_metric</code>: <code>str</code>, Optional, specifies the evaluation metric used to score
    different configuration during the model selection process, can be "BIC" or "MSLL",
    default is "MSLL"
<code>val_ratio</code>: <code>float</code>, Optional, specifies the percentage of random validation data
    allocated to to compute the "BIC" metric, default is 0.2
<code>base_kernels</code>: Set[str], Optional, specifies the list of kernels to use for
    Compositional Kernel Search, can be "all", "restricted" or Set[str] object
    Set of available kernels are ["LIN", "M12", "M32", "M52", "PER", "RBF", "RQF"],
    default is "restricted" and uses ["LIN", "M32", "M52", "PER", "RBF"]
<code>depth</code>: <code>int</code>, Optional, specifies the number of base kernels to be combined in
    the Compositional Kernel Search, depth=3 means the resulting kernel may be
    composed from three base kernels, e.g. "(LIN+PER)<em>RBF" or "(M12</em>RBF)+RQF",
    default is 1
<code>beam</code>: <code>int</code>, Optional, specifies the beam width of the Compositional Kernel Search
    algorithm, beam=1 is greedy search, beam=None performs breadth-first search and
    beam>1 perfroms beam search with the specified beam value, default is None
<code>resources_per_trial</code>: <code>dict</code>, Optional, The amount of CPU and GPU resources allocated
    to each trial of model selection, default is {"cpu": 1, "gpu": 0}</li>
<li><code>seed</code>: <code>int</code>, Optional, specifies the seed for the random number generator</li>
</ul>

<h2 id="example">Example</h2>

<p>Train using a local <code>json</code> parameters file:</p>

<div class="pdoc-code codehilite">
<pre><span></span><code><span class="kn">import</span> <span class="nn">twinlab</span> <span class="k">as</span> <span class="nn">tl</span>

<span class="n">tl</span><span class="o">.</span><span class="n">train_campaign</span><span class="p">(</span><span class="s2">&quot;path/to/params.json&quot;</span><span class="p">,</span> <span class="s2">&quot;my_campaign&quot;</span><span class="p">)</span>
</code></pre>
</div>

<p>Train via a <code>python</code> dictionary:</p>

<div class="pdoc-code codehilite">
<pre><span></span><code><span class="kn">import</span> <span class="nn">pandas</span> <span class="k">as</span> <span class="nn">pd</span>
<span class="kn">import</span> <span class="nn">twinlab</span> <span class="k">as</span> <span class="nn">tl</span>

<span class="n">df</span> <span class="o">=</span> <span class="n">pd</span><span class="o">.</span><span class="n">DataFrame</span><span class="p">({</span><span class="s1">&#39;X&#39;</span><span class="p">:</span> <span class="p">[</span><span class="mi">1</span><span class="p">,</span> <span class="mi">2</span><span class="p">,</span> <span class="mi">3</span><span class="p">,</span> <span class="mi">4</span><span class="p">],</span> <span class="s1">&#39;y&#39;</span><span class="p">:</span> <span class="p">[</span><span class="mi">1</span><span class="p">,</span> <span class="mi">4</span><span class="p">,</span> <span class="mi">9</span><span class="p">,</span> <span class="mi">16</span><span class="p">]})</span>
<span class="n">tl</span><span class="o">.</span><span class="n">upload_dataset</span><span class="p">(</span><span class="n">df</span><span class="p">,</span> <span class="s2">&quot;my_dataset&quot;</span><span class="p">)</span>
<span class="n">params</span> <span class="o">=</span> <span class="p">{</span>
    <span class="s2">&quot;dataset_id&quot;</span><span class="p">:</span> <span class="s2">&quot;my_dataset&quot;</span><span class="p">,</span>
    <span class="s2">&quot;inputs&quot;</span><span class="p">:</span> <span class="p">[</span><span class="s2">&quot;X&quot;</span><span class="p">],</span>
    <span class="s2">&quot;outputs&quot;</span><span class="p">:</span> <span class="p">[</span><span class="s2">&quot;y&quot;</span><span class="p">],</span>
<span class="p">}</span>
<span class="n">tl</span><span class="o">.</span><span class="n">train_campaign</span><span class="p">(</span><span class="n">params</span><span class="p">,</span> <span class="s2">&quot;my_campaign&quot;</span><span class="p">)</span>
</code></pre>
</div>
</div>


                </section>
                <section id="list_campaigns">
                            <input id="list_campaigns-view-source" class="view-source-toggle-state" type="checkbox" aria-hidden="true" tabindex="-1">
<div class="attr function">
            
        <span class="def">def</span>
        <span class="name">list_campaigns</span><span class="signature pdoc-code condensed">(<span class="param"><span class="n">verbose</span><span class="p">:</span> <span class="n">Optional</span><span class="p">[</span><span class="nb">bool</span><span class="p">]</span> <span class="o">=</span> <span class="kc">False</span>, </span><span class="param"><span class="n">debug</span><span class="p">:</span> <span class="n">Optional</span><span class="p">[</span><span class="nb">bool</span><span class="p">]</span> <span class="o">=</span> <span class="kc">False</span></span><span class="return-annotation">) -> <span class="nb">list</span>:</span></span>

                <label class="view-source-button" for="list_campaigns-view-source"><span>View Source</span></label>

    </div>
    <a class="headerlink" href="#list_campaigns"></a>
            <div class="pdoc-code codehilite"><pre><span></span><span id="list_campaigns-550"><a href="#list_campaigns-550"><span class="linenos">550</span></a><span class="k">def</span> <span class="nf">list_campaigns</span><span class="p">(</span>
</span><span id="list_campaigns-551"><a href="#list_campaigns-551"><span class="linenos">551</span></a>    <span class="n">verbose</span><span class="p">:</span> <span class="n">Optional</span><span class="p">[</span><span class="nb">bool</span><span class="p">]</span> <span class="o">=</span> <span class="kc">False</span><span class="p">,</span> <span class="n">debug</span><span class="p">:</span> <span class="n">Optional</span><span class="p">[</span><span class="nb">bool</span><span class="p">]</span> <span class="o">=</span> <span class="kc">False</span>
</span><span id="list_campaigns-552"><a href="#list_campaigns-552"><span class="linenos">552</span></a><span class="p">)</span> <span class="o">-&gt;</span> <span class="nb">list</span><span class="p">:</span>
</span><span id="list_campaigns-553"><a href="#list_campaigns-553"><span class="linenos">553</span></a><span class="w">    </span><span class="sd">&quot;&quot;&quot;</span>
</span><span id="list_campaigns-554"><a href="#list_campaigns-554"><span class="linenos">554</span></a><span class="sd">    # List campaigns</span>
</span><span id="list_campaigns-555"><a href="#list_campaigns-555"><span class="linenos">555</span></a>
</span><span id="list_campaigns-556"><a href="#list_campaigns-556"><span class="linenos">556</span></a><span class="sd">    List campaigns that have been completed to the `twinLab` cloud.</span>
</span><span id="list_campaigns-557"><a href="#list_campaigns-557"><span class="linenos">557</span></a>
</span><span id="list_campaigns-558"><a href="#list_campaigns-558"><span class="linenos">558</span></a><span class="sd">    ## Arguments</span>
</span><span id="list_campaigns-559"><a href="#list_campaigns-559"><span class="linenos">559</span></a>
</span><span id="list_campaigns-560"><a href="#list_campaigns-560"><span class="linenos">560</span></a><span class="sd">    - `verbose`: `bool`, Optional,determining level of information returned to the user</span>
</span><span id="list_campaigns-561"><a href="#list_campaigns-561"><span class="linenos">561</span></a><span class="sd">    - `debug`: `bool`, Optional, determining level of information logged on the server</span>
</span><span id="list_campaigns-562"><a href="#list_campaigns-562"><span class="linenos">562</span></a>
</span><span id="list_campaigns-563"><a href="#list_campaigns-563"><span class="linenos">563</span></a><span class="sd">    ## Returns</span>
</span><span id="list_campaigns-564"><a href="#list_campaigns-564"><span class="linenos">564</span></a>
</span><span id="list_campaigns-565"><a href="#list_campaigns-565"><span class="linenos">565</span></a><span class="sd">    - A `list` of `str` campaign ids</span>
</span><span id="list_campaigns-566"><a href="#list_campaigns-566"><span class="linenos">566</span></a>
</span><span id="list_campaigns-567"><a href="#list_campaigns-567"><span class="linenos">567</span></a><span class="sd">    ## Example</span>
</span><span id="list_campaigns-568"><a href="#list_campaigns-568"><span class="linenos">568</span></a>
</span><span id="list_campaigns-569"><a href="#list_campaigns-569"><span class="linenos">569</span></a><span class="sd">    ```python</span>
</span><span id="list_campaigns-570"><a href="#list_campaigns-570"><span class="linenos">570</span></a><span class="sd">    import twinlab as tl</span>
</span><span id="list_campaigns-571"><a href="#list_campaigns-571"><span class="linenos">571</span></a>
</span><span id="list_campaigns-572"><a href="#list_campaigns-572"><span class="linenos">572</span></a><span class="sd">    campaigns = tl.list_campaigns()</span>
</span><span id="list_campaigns-573"><a href="#list_campaigns-573"><span class="linenos">573</span></a><span class="sd">    print(campaigns)</span>
</span><span id="list_campaigns-574"><a href="#list_campaigns-574"><span class="linenos">574</span></a><span class="sd">    ```</span>
</span><span id="list_campaigns-575"><a href="#list_campaigns-575"><span class="linenos">575</span></a><span class="sd">    &quot;&quot;&quot;</span>
</span><span id="list_campaigns-576"><a href="#list_campaigns-576"><span class="linenos">576</span></a>    <span class="n">response</span> <span class="o">=</span> <span class="n">api</span><span class="o">.</span><span class="n">list_models</span><span class="p">(</span><span class="n">verbose</span><span class="o">=</span><span class="n">debug</span><span class="p">)</span>
</span><span id="list_campaigns-577"><a href="#list_campaigns-577"><span class="linenos">577</span></a>    <span class="n">campaigns</span> <span class="o">=</span> <span class="n">get_value_from_body</span><span class="p">(</span><span class="s2">&quot;models&quot;</span><span class="p">,</span> <span class="n">response</span><span class="p">)</span>
</span><span id="list_campaigns-578"><a href="#list_campaigns-578"><span class="linenos">578</span></a>    <span class="k">if</span> <span class="n">verbose</span><span class="p">:</span>
</span><span id="list_campaigns-579"><a href="#list_campaigns-579"><span class="linenos">579</span></a>        <span class="nb">print</span><span class="p">(</span><span class="s2">&quot;Trained models:&quot;</span><span class="p">)</span>
</span><span id="list_campaigns-580"><a href="#list_campaigns-580"><span class="linenos">580</span></a>        <span class="n">pprint</span><span class="p">(</span><span class="n">campaigns</span><span class="p">,</span> <span class="n">compact</span><span class="o">=</span><span class="kc">True</span><span class="p">,</span> <span class="n">sort_dicts</span><span class="o">=</span><span class="kc">False</span><span class="p">)</span>
</span><span id="list_campaigns-581"><a href="#list_campaigns-581"><span class="linenos">581</span></a>    <span class="k">return</span> <span class="n">campaigns</span>
</span></pre></div>


            <div class="docstring"><h1 id="list-campaigns">List campaigns</h1>

<p>List campaigns that have been completed to the <code>twinLab</code> cloud.</p>

<h2 id="arguments">Arguments</h2>

<ul>
<li><code>verbose</code>: <code>bool</code>, Optional,determining level of information returned to the user</li>
<li><code>debug</code>: <code>bool</code>, Optional, determining level of information logged on the server</li>
</ul>

<h2 id="returns">Returns</h2>

<ul>
<li>A <code>list</code> of <code>str</code> campaign ids</li>
</ul>

<h2 id="example">Example</h2>

<div class="pdoc-code codehilite">
<pre><span></span><code><span class="kn">import</span> <span class="nn">twinlab</span> <span class="k">as</span> <span class="nn">tl</span>

<span class="n">campaigns</span> <span class="o">=</span> <span class="n">tl</span><span class="o">.</span><span class="n">list_campaigns</span><span class="p">()</span>
<span class="nb">print</span><span class="p">(</span><span class="n">campaigns</span><span class="p">)</span>
</code></pre>
</div>
</div>


                </section>
                <section id="view_campaign">
                            <input id="view_campaign-view-source" class="view-source-toggle-state" type="checkbox" aria-hidden="true" tabindex="-1">
<div class="attr function">
            
        <span class="def">def</span>
        <span class="name">view_campaign</span><span class="signature pdoc-code multiline">(<span class="param">	<span class="n">campaign_id</span><span class="p">:</span> <span class="nb">str</span>,</span><span class="param">	<span class="n">verbose</span><span class="p">:</span> <span class="n">Optional</span><span class="p">[</span><span class="nb">bool</span><span class="p">]</span> <span class="o">=</span> <span class="kc">False</span>,</span><span class="param">	<span class="n">debug</span><span class="p">:</span> <span class="n">Optional</span><span class="p">[</span><span class="nb">bool</span><span class="p">]</span> <span class="o">=</span> <span class="kc">False</span></span><span class="return-annotation">) -> <span class="nb">dict</span>:</span></span>

                <label class="view-source-button" for="view_campaign-view-source"><span>View Source</span></label>

    </div>
    <a class="headerlink" href="#view_campaign"></a>
            <div class="pdoc-code codehilite"><pre><span></span><span id="view_campaign-585"><a href="#view_campaign-585"><span class="linenos">585</span></a><span class="k">def</span> <span class="nf">view_campaign</span><span class="p">(</span>
</span><span id="view_campaign-586"><a href="#view_campaign-586"><span class="linenos">586</span></a>    <span class="n">campaign_id</span><span class="p">:</span> <span class="nb">str</span><span class="p">,</span> <span class="n">verbose</span><span class="p">:</span> <span class="n">Optional</span><span class="p">[</span><span class="nb">bool</span><span class="p">]</span> <span class="o">=</span> <span class="kc">False</span><span class="p">,</span> <span class="n">debug</span><span class="p">:</span> <span class="n">Optional</span><span class="p">[</span><span class="nb">bool</span><span class="p">]</span> <span class="o">=</span> <span class="kc">False</span>
</span><span id="view_campaign-587"><a href="#view_campaign-587"><span class="linenos">587</span></a><span class="p">)</span> <span class="o">-&gt;</span> <span class="nb">dict</span><span class="p">:</span>
</span><span id="view_campaign-588"><a href="#view_campaign-588"><span class="linenos">588</span></a><span class="w">    </span><span class="sd">&quot;&quot;&quot;</span>
</span><span id="view_campaign-589"><a href="#view_campaign-589"><span class="linenos">589</span></a><span class="sd">    # View campaign</span>
</span><span id="view_campaign-590"><a href="#view_campaign-590"><span class="linenos">590</span></a>
</span><span id="view_campaign-591"><a href="#view_campaign-591"><span class="linenos">591</span></a><span class="sd">    View a campaign that exists on the twinLab cloud.</span>
</span><span id="view_campaign-592"><a href="#view_campaign-592"><span class="linenos">592</span></a>
</span><span id="view_campaign-593"><a href="#view_campaign-593"><span class="linenos">593</span></a><span class="sd">    ## Arguments</span>
</span><span id="view_campaign-594"><a href="#view_campaign-594"><span class="linenos">594</span></a>
</span><span id="view_campaign-595"><a href="#view_campaign-595"><span class="linenos">595</span></a><span class="sd">    - `campaign_id`: `str`; name for the model when saved to the twinLab cloud</span>
</span><span id="view_campaign-596"><a href="#view_campaign-596"><span class="linenos">596</span></a><span class="sd">    - `verbose`: `bool`, Optional, determining level of information returned to the user</span>
</span><span id="view_campaign-597"><a href="#view_campaign-597"><span class="linenos">597</span></a><span class="sd">    - `debug`: `bool`, Optional, determining level of information logged on the server</span>
</span><span id="view_campaign-598"><a href="#view_campaign-598"><span class="linenos">598</span></a>
</span><span id="view_campaign-599"><a href="#view_campaign-599"><span class="linenos">599</span></a><span class="sd">    ## Returns</span>
</span><span id="view_campaign-600"><a href="#view_campaign-600"><span class="linenos">600</span></a>
</span><span id="view_campaign-601"><a href="#view_campaign-601"><span class="linenos">601</span></a><span class="sd">    - `dict` containing the campaign training parameters.</span>
</span><span id="view_campaign-602"><a href="#view_campaign-602"><span class="linenos">602</span></a>
</span><span id="view_campaign-603"><a href="#view_campaign-603"><span class="linenos">603</span></a><span class="sd">    ## Example</span>
</span><span id="view_campaign-604"><a href="#view_campaign-604"><span class="linenos">604</span></a>
</span><span id="view_campaign-605"><a href="#view_campaign-605"><span class="linenos">605</span></a><span class="sd">    ```python</span>
</span><span id="view_campaign-606"><a href="#view_campaign-606"><span class="linenos">606</span></a><span class="sd">    import pandas as pd</span>
</span><span id="view_campaign-607"><a href="#view_campaign-607"><span class="linenos">607</span></a><span class="sd">    import twinlab as tl</span>
</span><span id="view_campaign-608"><a href="#view_campaign-608"><span class="linenos">608</span></a>
</span><span id="view_campaign-609"><a href="#view_campaign-609"><span class="linenos">609</span></a><span class="sd">    df = pd.DataFrame({&#39;X&#39;: [1, 2, 3, 4], &#39;y&#39;: [1, 4, 9, 16]})</span>
</span><span id="view_campaign-610"><a href="#view_campaign-610"><span class="linenos">610</span></a><span class="sd">    tl.upload_dataset(df, &quot;my_dataset&quot;)</span>
</span><span id="view_campaign-611"><a href="#view_campaign-611"><span class="linenos">611</span></a><span class="sd">    params = {</span>
</span><span id="view_campaign-612"><a href="#view_campaign-612"><span class="linenos">612</span></a><span class="sd">        &quot;dataset_id&quot;: &quot;my_dataset&quot;,</span>
</span><span id="view_campaign-613"><a href="#view_campaign-613"><span class="linenos">613</span></a><span class="sd">        &quot;inputs&quot;: [&quot;X&quot;],</span>
</span><span id="view_campaign-614"><a href="#view_campaign-614"><span class="linenos">614</span></a><span class="sd">        &quot;outputs&quot;: [&quot;y&quot;],</span>
</span><span id="view_campaign-615"><a href="#view_campaign-615"><span class="linenos">615</span></a><span class="sd">    }</span>
</span><span id="view_campaign-616"><a href="#view_campaign-616"><span class="linenos">616</span></a><span class="sd">    tl.train_campaign(params, &quot;my_campaign&quot;)</span>
</span><span id="view_campaign-617"><a href="#view_campaign-617"><span class="linenos">617</span></a><span class="sd">    params = tl.view_campaign(&quot;my_campaign&quot;)</span>
</span><span id="view_campaign-618"><a href="#view_campaign-618"><span class="linenos">618</span></a><span class="sd">    print(params)</span>
</span><span id="view_campaign-619"><a href="#view_campaign-619"><span class="linenos">619</span></a><span class="sd">    ```</span>
</span><span id="view_campaign-620"><a href="#view_campaign-620"><span class="linenos">620</span></a><span class="sd">    &quot;&quot;&quot;</span>
</span><span id="view_campaign-621"><a href="#view_campaign-621"><span class="linenos">621</span></a>    <span class="n">response</span> <span class="o">=</span> <span class="n">api</span><span class="o">.</span><span class="n">view_model</span><span class="p">(</span><span class="n">campaign_id</span><span class="p">,</span> <span class="n">verbose</span><span class="o">=</span><span class="n">debug</span><span class="p">)</span>
</span><span id="view_campaign-622"><a href="#view_campaign-622"><span class="linenos">622</span></a>    <span class="n">model_parameters</span> <span class="o">=</span> <span class="n">response</span>
</span><span id="view_campaign-623"><a href="#view_campaign-623"><span class="linenos">623</span></a>    <span class="k">if</span> <span class="n">verbose</span><span class="p">:</span>
</span><span id="view_campaign-624"><a href="#view_campaign-624"><span class="linenos">624</span></a>        <span class="nb">print</span><span class="p">(</span><span class="s2">&quot;Campaign summary:&quot;</span><span class="p">)</span>
</span><span id="view_campaign-625"><a href="#view_campaign-625"><span class="linenos">625</span></a>        <span class="n">pprint</span><span class="p">(</span><span class="n">model_parameters</span><span class="p">,</span> <span class="n">compact</span><span class="o">=</span><span class="kc">True</span><span class="p">,</span> <span class="n">sort_dicts</span><span class="o">=</span><span class="kc">False</span><span class="p">)</span>
</span><span id="view_campaign-626"><a href="#view_campaign-626"><span class="linenos">626</span></a>    <span class="k">return</span> <span class="n">model_parameters</span>
</span></pre></div>


            <div class="docstring"><h1 id="view-campaign">View campaign</h1>

<p>View a campaign that exists on the twinLab cloud.</p>

<h2 id="arguments">Arguments</h2>

<ul>
<li><code>campaign_id</code>: <code>str</code>; name for the model when saved to the twinLab cloud</li>
<li><code>verbose</code>: <code>bool</code>, Optional, determining level of information returned to the user</li>
<li><code>debug</code>: <code>bool</code>, Optional, determining level of information logged on the server</li>
</ul>

<h2 id="returns">Returns</h2>

<ul>
<li><code>dict</code> containing the campaign training parameters.</li>
</ul>

<h2 id="example">Example</h2>

<div class="pdoc-code codehilite">
<pre><span></span><code><span class="kn">import</span> <span class="nn">pandas</span> <span class="k">as</span> <span class="nn">pd</span>
<span class="kn">import</span> <span class="nn">twinlab</span> <span class="k">as</span> <span class="nn">tl</span>

<span class="n">df</span> <span class="o">=</span> <span class="n">pd</span><span class="o">.</span><span class="n">DataFrame</span><span class="p">({</span><span class="s1">&#39;X&#39;</span><span class="p">:</span> <span class="p">[</span><span class="mi">1</span><span class="p">,</span> <span class="mi">2</span><span class="p">,</span> <span class="mi">3</span><span class="p">,</span> <span class="mi">4</span><span class="p">],</span> <span class="s1">&#39;y&#39;</span><span class="p">:</span> <span class="p">[</span><span class="mi">1</span><span class="p">,</span> <span class="mi">4</span><span class="p">,</span> <span class="mi">9</span><span class="p">,</span> <span class="mi">16</span><span class="p">]})</span>
<span class="n">tl</span><span class="o">.</span><span class="n">upload_dataset</span><span class="p">(</span><span class="n">df</span><span class="p">,</span> <span class="s2">&quot;my_dataset&quot;</span><span class="p">)</span>
<span class="n">params</span> <span class="o">=</span> <span class="p">{</span>
    <span class="s2">&quot;dataset_id&quot;</span><span class="p">:</span> <span class="s2">&quot;my_dataset&quot;</span><span class="p">,</span>
    <span class="s2">&quot;inputs&quot;</span><span class="p">:</span> <span class="p">[</span><span class="s2">&quot;X&quot;</span><span class="p">],</span>
    <span class="s2">&quot;outputs&quot;</span><span class="p">:</span> <span class="p">[</span><span class="s2">&quot;y&quot;</span><span class="p">],</span>
<span class="p">}</span>
<span class="n">tl</span><span class="o">.</span><span class="n">train_campaign</span><span class="p">(</span><span class="n">params</span><span class="p">,</span> <span class="s2">&quot;my_campaign&quot;</span><span class="p">)</span>
<span class="n">params</span> <span class="o">=</span> <span class="n">tl</span><span class="o">.</span><span class="n">view_campaign</span><span class="p">(</span><span class="s2">&quot;my_campaign&quot;</span><span class="p">)</span>
<span class="nb">print</span><span class="p">(</span><span class="n">params</span><span class="p">)</span>
</code></pre>
</div>
</div>


                </section>
                <section id="query_campaign">
                            <input id="query_campaign-view-source" class="view-source-toggle-state" type="checkbox" aria-hidden="true" tabindex="-1">
<div class="attr function">
            
        <span class="def">def</span>
        <span class="name">query_campaign</span><span class="signature pdoc-code multiline">(<span class="param">	<span class="n">campaign_id</span><span class="p">:</span> <span class="nb">str</span>,</span><span class="param">	<span class="n">verbose</span><span class="p">:</span> <span class="n">Optional</span><span class="p">[</span><span class="nb">bool</span><span class="p">]</span> <span class="o">=</span> <span class="kc">False</span>,</span><span class="param">	<span class="n">debug</span><span class="p">:</span> <span class="n">Optional</span><span class="p">[</span><span class="nb">bool</span><span class="p">]</span> <span class="o">=</span> <span class="kc">False</span></span><span class="return-annotation">) -> <span class="nb">dict</span>:</span></span>

                <label class="view-source-button" for="query_campaign-view-source"><span>View Source</span></label>

    </div>
    <a class="headerlink" href="#query_campaign"></a>
            <div class="pdoc-code codehilite"><pre><span></span><span id="query_campaign-630"><a href="#query_campaign-630"><span class="linenos">630</span></a><span class="k">def</span> <span class="nf">query_campaign</span><span class="p">(</span>
</span><span id="query_campaign-631"><a href="#query_campaign-631"><span class="linenos">631</span></a>    <span class="n">campaign_id</span><span class="p">:</span> <span class="nb">str</span><span class="p">,</span> <span class="n">verbose</span><span class="p">:</span> <span class="n">Optional</span><span class="p">[</span><span class="nb">bool</span><span class="p">]</span> <span class="o">=</span> <span class="kc">False</span><span class="p">,</span> <span class="n">debug</span><span class="p">:</span> <span class="n">Optional</span><span class="p">[</span><span class="nb">bool</span><span class="p">]</span> <span class="o">=</span> <span class="kc">False</span>
</span><span id="query_campaign-632"><a href="#query_campaign-632"><span class="linenos">632</span></a><span class="p">)</span> <span class="o">-&gt;</span> <span class="nb">dict</span><span class="p">:</span>
</span><span id="query_campaign-633"><a href="#query_campaign-633"><span class="linenos">633</span></a><span class="w">    </span><span class="sd">&quot;&quot;&quot;</span>
</span><span id="query_campaign-634"><a href="#query_campaign-634"><span class="linenos">634</span></a><span class="sd">    # Query campaign</span>
</span><span id="query_campaign-635"><a href="#query_campaign-635"><span class="linenos">635</span></a>
</span><span id="query_campaign-636"><a href="#query_campaign-636"><span class="linenos">636</span></a><span class="sd">    Get summary statistics for a pre-trained campaign in the `twinLab` cloud.</span>
</span><span id="query_campaign-637"><a href="#query_campaign-637"><span class="linenos">637</span></a>
</span><span id="query_campaign-638"><a href="#query_campaign-638"><span class="linenos">638</span></a><span class="sd">    ## Arguments</span>
</span><span id="query_campaign-639"><a href="#query_campaign-639"><span class="linenos">639</span></a>
</span><span id="query_campaign-640"><a href="#query_campaign-640"><span class="linenos">640</span></a><span class="sd">    - `campaign_id`: `str`; name of trained campaign to query</span>
</span><span id="query_campaign-641"><a href="#query_campaign-641"><span class="linenos">641</span></a><span class="sd">    - `verbose`: `bool`, Optional, determining level of information returned to the user</span>
</span><span id="query_campaign-642"><a href="#query_campaign-642"><span class="linenos">642</span></a><span class="sd">    - `debug`: `bool`, Optional, determining level of information logged on the server</span>
</span><span id="query_campaign-643"><a href="#query_campaign-643"><span class="linenos">643</span></a>
</span><span id="query_campaign-644"><a href="#query_campaign-644"><span class="linenos">644</span></a><span class="sd">    ## Returns</span>
</span><span id="query_campaign-645"><a href="#query_campaign-645"><span class="linenos">645</span></a>
</span><span id="query_campaign-646"><a href="#query_campaign-646"><span class="linenos">646</span></a><span class="sd">    - `dict` containing summary statistics for the pre-trained campaign.</span>
</span><span id="query_campaign-647"><a href="#query_campaign-647"><span class="linenos">647</span></a>
</span><span id="query_campaign-648"><a href="#query_campaign-648"><span class="linenos">648</span></a><span class="sd">    ## Example</span>
</span><span id="query_campaign-649"><a href="#query_campaign-649"><span class="linenos">649</span></a>
</span><span id="query_campaign-650"><a href="#query_campaign-650"><span class="linenos">650</span></a><span class="sd">    ```python</span>
</span><span id="query_campaign-651"><a href="#query_campaign-651"><span class="linenos">651</span></a><span class="sd">    import pandas as pd</span>
</span><span id="query_campaign-652"><a href="#query_campaign-652"><span class="linenos">652</span></a><span class="sd">    import twinlab as tl</span>
</span><span id="query_campaign-653"><a href="#query_campaign-653"><span class="linenos">653</span></a>
</span><span id="query_campaign-654"><a href="#query_campaign-654"><span class="linenos">654</span></a><span class="sd">    df = pd.DataFrame({&#39;X&#39;: [1, 2, 3, 4], &#39;y&#39;: [1, 4, 9, 16]})</span>
</span><span id="query_campaign-655"><a href="#query_campaign-655"><span class="linenos">655</span></a><span class="sd">    tl.upload_dataset(df, &quot;my_dataset&quot;)</span>
</span><span id="query_campaign-656"><a href="#query_campaign-656"><span class="linenos">656</span></a><span class="sd">    params = {</span>
</span><span id="query_campaign-657"><a href="#query_campaign-657"><span class="linenos">657</span></a><span class="sd">        &quot;dataset_id&quot;: &quot;my_dataset&quot;,</span>
</span><span id="query_campaign-658"><a href="#query_campaign-658"><span class="linenos">658</span></a><span class="sd">        &quot;inputs&quot;: [&quot;X&quot;],</span>
</span><span id="query_campaign-659"><a href="#query_campaign-659"><span class="linenos">659</span></a><span class="sd">        &quot;outputs&quot;: [&quot;y&quot;],</span>
</span><span id="query_campaign-660"><a href="#query_campaign-660"><span class="linenos">660</span></a><span class="sd">    }</span>
</span><span id="query_campaign-661"><a href="#query_campaign-661"><span class="linenos">661</span></a><span class="sd">    tl.train_campaign(params, &quot;my_campaign&quot;)</span>
</span><span id="query_campaign-662"><a href="#query_campaign-662"><span class="linenos">662</span></a><span class="sd">    info = tl.query_campaign(&quot;my_campaign&quot;)</span>
</span><span id="query_campaign-663"><a href="#query_campaign-663"><span class="linenos">663</span></a><span class="sd">    print(info)</span>
</span><span id="query_campaign-664"><a href="#query_campaign-664"><span class="linenos">664</span></a><span class="sd">    ```</span>
</span><span id="query_campaign-665"><a href="#query_campaign-665"><span class="linenos">665</span></a><span class="sd">    &quot;&quot;&quot;</span>
</span><span id="query_campaign-666"><a href="#query_campaign-666"><span class="linenos">666</span></a>    <span class="n">response</span> <span class="o">=</span> <span class="n">api</span><span class="o">.</span><span class="n">summarise_model</span><span class="p">(</span><span class="n">campaign_id</span><span class="p">,</span> <span class="n">verbose</span><span class="o">=</span><span class="n">debug</span><span class="p">)</span>
</span><span id="query_campaign-667"><a href="#query_campaign-667"><span class="linenos">667</span></a>    <span class="n">summary</span> <span class="o">=</span> <span class="n">response</span>
</span><span id="query_campaign-668"><a href="#query_campaign-668"><span class="linenos">668</span></a>    <span class="c1"># summary = json.loads(response[&quot;model_summary&quot;]) # TODO: This should work eventually</span>
</span><span id="query_campaign-669"><a href="#query_campaign-669"><span class="linenos">669</span></a>    <span class="k">if</span> <span class="n">verbose</span><span class="p">:</span>
</span><span id="query_campaign-670"><a href="#query_campaign-670"><span class="linenos">670</span></a>        <span class="nb">print</span><span class="p">(</span><span class="s2">&quot;Model summary:&quot;</span><span class="p">)</span>
</span><span id="query_campaign-671"><a href="#query_campaign-671"><span class="linenos">671</span></a>        <span class="n">pprint</span><span class="p">(</span><span class="n">summary</span><span class="p">,</span> <span class="n">compact</span><span class="o">=</span><span class="kc">True</span><span class="p">,</span> <span class="n">sort_dicts</span><span class="o">=</span><span class="kc">False</span><span class="p">)</span>
</span><span id="query_campaign-672"><a href="#query_campaign-672"><span class="linenos">672</span></a>    <span class="k">return</span> <span class="n">summary</span>
</span></pre></div>


            <div class="docstring"><h1 id="query-campaign">Query campaign</h1>

<p>Get summary statistics for a pre-trained campaign in the <code>twinLab</code> cloud.</p>

<h2 id="arguments">Arguments</h2>

<ul>
<li><code>campaign_id</code>: <code>str</code>; name of trained campaign to query</li>
<li><code>verbose</code>: <code>bool</code>, Optional, determining level of information returned to the user</li>
<li><code>debug</code>: <code>bool</code>, Optional, determining level of information logged on the server</li>
</ul>

<h2 id="returns">Returns</h2>

<ul>
<li><code>dict</code> containing summary statistics for the pre-trained campaign.</li>
</ul>

<h2 id="example">Example</h2>

<div class="pdoc-code codehilite">
<pre><span></span><code><span class="kn">import</span> <span class="nn">pandas</span> <span class="k">as</span> <span class="nn">pd</span>
<span class="kn">import</span> <span class="nn">twinlab</span> <span class="k">as</span> <span class="nn">tl</span>

<span class="n">df</span> <span class="o">=</span> <span class="n">pd</span><span class="o">.</span><span class="n">DataFrame</span><span class="p">({</span><span class="s1">&#39;X&#39;</span><span class="p">:</span> <span class="p">[</span><span class="mi">1</span><span class="p">,</span> <span class="mi">2</span><span class="p">,</span> <span class="mi">3</span><span class="p">,</span> <span class="mi">4</span><span class="p">],</span> <span class="s1">&#39;y&#39;</span><span class="p">:</span> <span class="p">[</span><span class="mi">1</span><span class="p">,</span> <span class="mi">4</span><span class="p">,</span> <span class="mi">9</span><span class="p">,</span> <span class="mi">16</span><span class="p">]})</span>
<span class="n">tl</span><span class="o">.</span><span class="n">upload_dataset</span><span class="p">(</span><span class="n">df</span><span class="p">,</span> <span class="s2">&quot;my_dataset&quot;</span><span class="p">)</span>
<span class="n">params</span> <span class="o">=</span> <span class="p">{</span>
    <span class="s2">&quot;dataset_id&quot;</span><span class="p">:</span> <span class="s2">&quot;my_dataset&quot;</span><span class="p">,</span>
    <span class="s2">&quot;inputs&quot;</span><span class="p">:</span> <span class="p">[</span><span class="s2">&quot;X&quot;</span><span class="p">],</span>
    <span class="s2">&quot;outputs&quot;</span><span class="p">:</span> <span class="p">[</span><span class="s2">&quot;y&quot;</span><span class="p">],</span>
<span class="p">}</span>
<span class="n">tl</span><span class="o">.</span><span class="n">train_campaign</span><span class="p">(</span><span class="n">params</span><span class="p">,</span> <span class="s2">&quot;my_campaign&quot;</span><span class="p">)</span>
<span class="n">info</span> <span class="o">=</span> <span class="n">tl</span><span class="o">.</span><span class="n">query_campaign</span><span class="p">(</span><span class="s2">&quot;my_campaign&quot;</span><span class="p">)</span>
<span class="nb">print</span><span class="p">(</span><span class="n">info</span><span class="p">)</span>
</code></pre>
</div>
</div>


                </section>
                <section id="predict_campaign">
                            <input id="predict_campaign-view-source" class="view-source-toggle-state" type="checkbox" aria-hidden="true" tabindex="-1">
<div class="attr function">
            
        <span class="def">def</span>
        <span class="name">predict_campaign</span><span class="signature pdoc-code multiline">(<span class="param">	<span class="n">filepath_or_df</span><span class="p">:</span> <span class="n">Union</span><span class="p">[</span><span class="nb">str</span><span class="p">,</span> <span class="n">pandas</span><span class="o">.</span><span class="n">core</span><span class="o">.</span><span class="n">frame</span><span class="o">.</span><span class="n">DataFrame</span><span class="p">]</span>,</span><span class="param">	<span class="n">campaign_id</span><span class="p">:</span> <span class="nb">str</span>,</span><span class="param">	<span class="n">processor</span><span class="p">:</span> <span class="n">Optional</span><span class="p">[</span><span class="nb">str</span><span class="p">]</span> <span class="o">=</span> <span class="s1">&#39;cpu&#39;</span>,</span><span class="param">	<span class="n">verbose</span><span class="p">:</span> <span class="n">Optional</span><span class="p">[</span><span class="nb">bool</span><span class="p">]</span> <span class="o">=</span> <span class="kc">False</span>,</span><span class="param">	<span class="n">debug</span><span class="p">:</span> <span class="n">Optional</span><span class="p">[</span><span class="nb">bool</span><span class="p">]</span> <span class="o">=</span> <span class="kc">False</span></span><span class="return-annotation">) -> <span class="n">Tuple</span><span class="p">[</span><span class="n">pandas</span><span class="o">.</span><span class="n">core</span><span class="o">.</span><span class="n">frame</span><span class="o">.</span><span class="n">DataFrame</span><span class="p">,</span> <span class="n">pandas</span><span class="o">.</span><span class="n">core</span><span class="o">.</span><span class="n">frame</span><span class="o">.</span><span class="n">DataFrame</span><span class="p">]</span>:</span></span>

                <label class="view-source-button" for="predict_campaign-view-source"><span>View Source</span></label>

    </div>
    <a class="headerlink" href="#predict_campaign"></a>
            <div class="pdoc-code codehilite"><pre><span></span><span id="predict_campaign-676"><a href="#predict_campaign-676"><span class="linenos">676</span></a><span class="k">def</span> <span class="nf">predict_campaign</span><span class="p">(</span>
</span><span id="predict_campaign-677"><a href="#predict_campaign-677"><span class="linenos">677</span></a>    <span class="n">filepath_or_df</span><span class="p">:</span> <span class="n">Union</span><span class="p">[</span><span class="nb">str</span><span class="p">,</span> <span class="n">pd</span><span class="o">.</span><span class="n">DataFrame</span><span class="p">],</span>
</span><span id="predict_campaign-678"><a href="#predict_campaign-678"><span class="linenos">678</span></a>    <span class="n">campaign_id</span><span class="p">:</span> <span class="nb">str</span><span class="p">,</span>
</span><span id="predict_campaign-679"><a href="#predict_campaign-679"><span class="linenos">679</span></a>    <span class="n">processor</span><span class="p">:</span> <span class="n">Optional</span><span class="p">[</span><span class="nb">str</span><span class="p">]</span> <span class="o">=</span> <span class="s2">&quot;cpu&quot;</span><span class="p">,</span>
</span><span id="predict_campaign-680"><a href="#predict_campaign-680"><span class="linenos">680</span></a>    <span class="n">verbose</span><span class="p">:</span> <span class="n">Optional</span><span class="p">[</span><span class="nb">bool</span><span class="p">]</span> <span class="o">=</span> <span class="kc">False</span><span class="p">,</span>
</span><span id="predict_campaign-681"><a href="#predict_campaign-681"><span class="linenos">681</span></a>    <span class="n">debug</span><span class="p">:</span> <span class="n">Optional</span><span class="p">[</span><span class="nb">bool</span><span class="p">]</span> <span class="o">=</span> <span class="kc">False</span><span class="p">,</span>
</span><span id="predict_campaign-682"><a href="#predict_campaign-682"><span class="linenos">682</span></a><span class="p">)</span> <span class="o">-&gt;</span> <span class="n">Tuple</span><span class="p">[</span><span class="n">pd</span><span class="o">.</span><span class="n">DataFrame</span><span class="p">,</span> <span class="n">pd</span><span class="o">.</span><span class="n">DataFrame</span><span class="p">]:</span>
</span><span id="predict_campaign-683"><a href="#predict_campaign-683"><span class="linenos">683</span></a><span class="w">    </span><span class="sd">&quot;&quot;&quot;</span>
</span><span id="predict_campaign-684"><a href="#predict_campaign-684"><span class="linenos">684</span></a><span class="sd">    # Predict campaign</span>
</span><span id="predict_campaign-685"><a href="#predict_campaign-685"><span class="linenos">685</span></a>
</span><span id="predict_campaign-686"><a href="#predict_campaign-686"><span class="linenos">686</span></a><span class="sd">    Make predictions from a pre-trained model that exists on the `twinLab` cloud.</span>
</span><span id="predict_campaign-687"><a href="#predict_campaign-687"><span class="linenos">687</span></a>
</span><span id="predict_campaign-688"><a href="#predict_campaign-688"><span class="linenos">688</span></a><span class="sd">    ## Arguments</span>
</span><span id="predict_campaign-689"><a href="#predict_campaign-689"><span class="linenos">689</span></a>
</span><span id="predict_campaign-690"><a href="#predict_campaign-690"><span class="linenos">690</span></a><span class="sd">    - `filepath_or_df`: `str`; location of csv dataset on local machine for evaluation</span>
</span><span id="predict_campaign-691"><a href="#predict_campaign-691"><span class="linenos">691</span></a><span class="sd">        or `pandas` dataframe</span>
</span><span id="predict_campaign-692"><a href="#predict_campaign-692"><span class="linenos">692</span></a><span class="sd">    - `campaign_id`: `str`; name of pre-trained campaign to use for predictions</span>
</span><span id="predict_campaign-693"><a href="#predict_campaign-693"><span class="linenos">693</span></a><span class="sd">    - `processor`: `str`, Optional, processor to use for sampling (&quot;cpu&quot;; &quot;gpu&quot;)</span>
</span><span id="predict_campaign-694"><a href="#predict_campaign-694"><span class="linenos">694</span></a><span class="sd">    - `verbose`: `bool`, Optional, determining level of information returned to the user</span>
</span><span id="predict_campaign-695"><a href="#predict_campaign-695"><span class="linenos">695</span></a><span class="sd">    - `debug`: `bool`, Optional, determining level of information logged on the server</span>
</span><span id="predict_campaign-696"><a href="#predict_campaign-696"><span class="linenos">696</span></a>
</span><span id="predict_campaign-697"><a href="#predict_campaign-697"><span class="linenos">697</span></a><span class="sd">    **NOTE:** Evaluation data must be a CSV file, or a `pandas` dataframe that is interpretable as a CSV.</span>
</span><span id="predict_campaign-698"><a href="#predict_campaign-698"><span class="linenos">698</span></a>
</span><span id="predict_campaign-699"><a href="#predict_campaign-699"><span class="linenos">699</span></a><span class="sd">    ## Returns</span>
</span><span id="predict_campaign-700"><a href="#predict_campaign-700"><span class="linenos">700</span></a>
</span><span id="predict_campaign-701"><a href="#predict_campaign-701"><span class="linenos">701</span></a><span class="sd">    - `tuple` containing:</span>
</span><span id="predict_campaign-702"><a href="#predict_campaign-702"><span class="linenos">702</span></a><span class="sd">        - `df_mean`: `pandas.DataFrame` containing mean predictions</span>
</span><span id="predict_campaign-703"><a href="#predict_campaign-703"><span class="linenos">703</span></a><span class="sd">        - `df_std`: `pandas.DataFrame` containing standard deviation predictions</span>
</span><span id="predict_campaign-704"><a href="#predict_campaign-704"><span class="linenos">704</span></a>
</span><span id="predict_campaign-705"><a href="#predict_campaign-705"><span class="linenos">705</span></a><span class="sd">    ## Example</span>
</span><span id="predict_campaign-706"><a href="#predict_campaign-706"><span class="linenos">706</span></a>
</span><span id="predict_campaign-707"><a href="#predict_campaign-707"><span class="linenos">707</span></a><span class="sd">    Using a local file:</span>
</span><span id="predict_campaign-708"><a href="#predict_campaign-708"><span class="linenos">708</span></a><span class="sd">    ```python</span>
</span><span id="predict_campaign-709"><a href="#predict_campaign-709"><span class="linenos">709</span></a><span class="sd">    import pandas as pd</span>
</span><span id="predict_campaign-710"><a href="#predict_campaign-710"><span class="linenos">710</span></a><span class="sd">    import twinlab as tl</span>
</span><span id="predict_campaign-711"><a href="#predict_campaign-711"><span class="linenos">711</span></a>
</span><span id="predict_campaign-712"><a href="#predict_campaign-712"><span class="linenos">712</span></a><span class="sd">    df = pd.DataFrame({&#39;X&#39;: [1, 2, 3, 4], &#39;y&#39;: [1, 4, 9, 16]})</span>
</span><span id="predict_campaign-713"><a href="#predict_campaign-713"><span class="linenos">713</span></a><span class="sd">    tl.upload_dataset(df, &quot;my_dataset&quot;)</span>
</span><span id="predict_campaign-714"><a href="#predict_campaign-714"><span class="linenos">714</span></a><span class="sd">    params = {</span>
</span><span id="predict_campaign-715"><a href="#predict_campaign-715"><span class="linenos">715</span></a><span class="sd">        &quot;dataset_id&quot;: &quot;my_dataset&quot;,</span>
</span><span id="predict_campaign-716"><a href="#predict_campaign-716"><span class="linenos">716</span></a><span class="sd">        &quot;inputs&quot;: [&quot;X&quot;],</span>
</span><span id="predict_campaign-717"><a href="#predict_campaign-717"><span class="linenos">717</span></a><span class="sd">        &quot;outputs&quot;: [&quot;y&quot;],</span>
</span><span id="predict_campaign-718"><a href="#predict_campaign-718"><span class="linenos">718</span></a><span class="sd">    }</span>
</span><span id="predict_campaign-719"><a href="#predict_campaign-719"><span class="linenos">719</span></a><span class="sd">    tl.train_campaign(params, &quot;my_campaign&quot;)</span>
</span><span id="predict_campaign-720"><a href="#predict_campaign-720"><span class="linenos">720</span></a><span class="sd">    filepath = &quot;path/to/data.csv&quot; # Local</span>
</span><span id="predict_campaign-721"><a href="#predict_campaign-721"><span class="linenos">721</span></a><span class="sd">    campaign_id = &#39;my_campaign&quot; # Pre-trained</span>
</span><span id="predict_campaign-722"><a href="#predict_campaign-722"><span class="linenos">722</span></a><span class="sd">    df_mean, df_std = tl.predict_campaign(filepath, campaign_id)</span>
</span><span id="predict_campaign-723"><a href="#predict_campaign-723"><span class="linenos">723</span></a><span class="sd">    print(df_mean)</span>
</span><span id="predict_campaign-724"><a href="#predict_campaign-724"><span class="linenos">724</span></a><span class="sd">    print(df_std)</span>
</span><span id="predict_campaign-725"><a href="#predict_campaign-725"><span class="linenos">725</span></a><span class="sd">    ```</span>
</span><span id="predict_campaign-726"><a href="#predict_campaign-726"><span class="linenos">726</span></a>
</span><span id="predict_campaign-727"><a href="#predict_campaign-727"><span class="linenos">727</span></a><span class="sd">    Using a `pandas` dataframe:</span>
</span><span id="predict_campaign-728"><a href="#predict_campaign-728"><span class="linenos">728</span></a><span class="sd">    ```python</span>
</span><span id="predict_campaign-729"><a href="#predict_campaign-729"><span class="linenos">729</span></a><span class="sd">    import pandas as pd</span>
</span><span id="predict_campaign-730"><a href="#predict_campaign-730"><span class="linenos">730</span></a><span class="sd">    import twinlab as tl</span>
</span><span id="predict_campaign-731"><a href="#predict_campaign-731"><span class="linenos">731</span></a>
</span><span id="predict_campaign-732"><a href="#predict_campaign-732"><span class="linenos">732</span></a><span class="sd">    df = pd.DataFrame({&#39;X&#39;: [1, 2, 3, 4], &#39;y&#39;: [1, 4, 9, 16]})</span>
</span><span id="predict_campaign-733"><a href="#predict_campaign-733"><span class="linenos">733</span></a><span class="sd">    tl.upload_dataset(df, &quot;my_dataset&quot;)</span>
</span><span id="predict_campaign-734"><a href="#predict_campaign-734"><span class="linenos">734</span></a><span class="sd">    params = {</span>
</span><span id="predict_campaign-735"><a href="#predict_campaign-735"><span class="linenos">735</span></a><span class="sd">        &quot;dataset_id&quot;: &quot;my_dataset&quot;,</span>
</span><span id="predict_campaign-736"><a href="#predict_campaign-736"><span class="linenos">736</span></a><span class="sd">        &quot;inputs&quot;: [&quot;X&quot;],</span>
</span><span id="predict_campaign-737"><a href="#predict_campaign-737"><span class="linenos">737</span></a><span class="sd">        &quot;outputs&quot;: [&quot;y&quot;],</span>
</span><span id="predict_campaign-738"><a href="#predict_campaign-738"><span class="linenos">738</span></a><span class="sd">    }</span>
</span><span id="predict_campaign-739"><a href="#predict_campaign-739"><span class="linenos">739</span></a><span class="sd">    tl.train_campaign(params, &quot;my_campaign&quot;)</span>
</span><span id="predict_campaign-740"><a href="#predict_campaign-740"><span class="linenos">740</span></a><span class="sd">    df = pd.DataFrame({&#39;X&#39;: [1.5, 2.5, 3.5]})</span>
</span><span id="predict_campaign-741"><a href="#predict_campaign-741"><span class="linenos">741</span></a><span class="sd">    tl.predict_campaign(df, &quot;my_campaign&quot;)</span>
</span><span id="predict_campaign-742"><a href="#predict_campaign-742"><span class="linenos">742</span></a><span class="sd">    ```</span>
</span><span id="predict_campaign-743"><a href="#predict_campaign-743"><span class="linenos">743</span></a><span class="sd">    &quot;&quot;&quot;</span>
</span><span id="predict_campaign-744"><a href="#predict_campaign-744"><span class="linenos">744</span></a>
</span><span id="predict_campaign-745"><a href="#predict_campaign-745"><span class="linenos">745</span></a>    <span class="n">csv</span> <span class="o">=</span> <span class="n">_use_campaign</span><span class="p">(</span>
</span><span id="predict_campaign-746"><a href="#predict_campaign-746"><span class="linenos">746</span></a>        <span class="n">campaign_id</span><span class="p">,</span>
</span><span id="predict_campaign-747"><a href="#predict_campaign-747"><span class="linenos">747</span></a>        <span class="n">method</span><span class="o">=</span><span class="s2">&quot;predict&quot;</span><span class="p">,</span>
</span><span id="predict_campaign-748"><a href="#predict_campaign-748"><span class="linenos">748</span></a>        <span class="n">filepath_or_df</span><span class="o">=</span><span class="n">filepath_or_df</span><span class="p">,</span>
</span><span id="predict_campaign-749"><a href="#predict_campaign-749"><span class="linenos">749</span></a>        <span class="n">processor</span><span class="o">=</span><span class="n">processor</span><span class="p">,</span>
</span><span id="predict_campaign-750"><a href="#predict_campaign-750"><span class="linenos">750</span></a>        <span class="n">verbose</span><span class="o">=</span><span class="n">verbose</span><span class="p">,</span>
</span><span id="predict_campaign-751"><a href="#predict_campaign-751"><span class="linenos">751</span></a>        <span class="n">debug</span><span class="o">=</span><span class="n">debug</span><span class="p">,</span>
</span><span id="predict_campaign-752"><a href="#predict_campaign-752"><span class="linenos">752</span></a>    <span class="p">)</span>
</span><span id="predict_campaign-753"><a href="#predict_campaign-753"><span class="linenos">753</span></a>    <span class="n">df</span> <span class="o">=</span> <span class="n">pd</span><span class="o">.</span><span class="n">read_csv</span><span class="p">(</span><span class="n">csv</span><span class="p">,</span> <span class="n">sep</span><span class="o">=</span><span class="s2">&quot;,&quot;</span><span class="p">)</span>
</span><span id="predict_campaign-754"><a href="#predict_campaign-754"><span class="linenos">754</span></a>    <span class="n">n</span> <span class="o">=</span> <span class="nb">len</span><span class="p">(</span><span class="n">df</span><span class="o">.</span><span class="n">columns</span><span class="p">)</span>
</span><span id="predict_campaign-755"><a href="#predict_campaign-755"><span class="linenos">755</span></a>    <span class="n">df_mean</span><span class="p">,</span> <span class="n">df_std</span> <span class="o">=</span> <span class="n">df</span><span class="o">.</span><span class="n">iloc</span><span class="p">[:,</span> <span class="p">:</span> <span class="n">n</span> <span class="o">//</span> <span class="mi">2</span><span class="p">],</span> <span class="n">df</span><span class="o">.</span><span class="n">iloc</span><span class="p">[:,</span> <span class="n">n</span> <span class="o">//</span> <span class="mi">2</span> <span class="p">:]</span>
</span><span id="predict_campaign-756"><a href="#predict_campaign-756"><span class="linenos">756</span></a>    <span class="n">df_std</span><span class="o">.</span><span class="n">columns</span> <span class="o">=</span> <span class="n">df_std</span><span class="o">.</span><span class="n">columns</span><span class="o">.</span><span class="n">str</span><span class="o">.</span><span class="n">removesuffix</span><span class="p">(</span><span class="s2">&quot; [std_dev]&quot;</span><span class="p">)</span>
</span><span id="predict_campaign-757"><a href="#predict_campaign-757"><span class="linenos">757</span></a>    <span class="k">if</span> <span class="n">verbose</span><span class="p">:</span>
</span><span id="predict_campaign-758"><a href="#predict_campaign-758"><span class="linenos">758</span></a>        <span class="nb">print</span><span class="p">(</span><span class="s2">&quot;Mean predictions:&quot;</span><span class="p">)</span>
</span><span id="predict_campaign-759"><a href="#predict_campaign-759"><span class="linenos">759</span></a>        <span class="nb">print</span><span class="p">(</span><span class="n">df_mean</span><span class="p">)</span>
</span><span id="predict_campaign-760"><a href="#predict_campaign-760"><span class="linenos">760</span></a>        <span class="nb">print</span><span class="p">(</span><span class="s2">&quot;Standard deviation predictions:&quot;</span><span class="p">)</span>
</span><span id="predict_campaign-761"><a href="#predict_campaign-761"><span class="linenos">761</span></a>        <span class="nb">print</span><span class="p">(</span><span class="n">df_std</span><span class="p">)</span>
</span><span id="predict_campaign-762"><a href="#predict_campaign-762"><span class="linenos">762</span></a>
</span><span id="predict_campaign-763"><a href="#predict_campaign-763"><span class="linenos">763</span></a>    <span class="k">return</span> <span class="n">df_mean</span><span class="p">,</span> <span class="n">df_std</span>
</span></pre></div>


            <div class="docstring"><h1 id="predict-campaign">Predict campaign</h1>

<p>Make predictions from a pre-trained model that exists on the <code>twinLab</code> cloud.</p>

<h2 id="arguments">Arguments</h2>

<ul>
<li><code>filepath_or_df</code>: <code>str</code>; location of csv dataset on local machine for evaluation
or <code>pandas</code> dataframe</li>
<li><code>campaign_id</code>: <code>str</code>; name of pre-trained campaign to use for predictions</li>
<li><code>processor</code>: <code>str</code>, Optional, processor to use for sampling ("cpu"; "gpu")</li>
<li><code>verbose</code>: <code>bool</code>, Optional, determining level of information returned to the user</li>
<li><code>debug</code>: <code>bool</code>, Optional, determining level of information logged on the server</li>
</ul>

<p><strong>NOTE:</strong> Evaluation data must be a CSV file, or a <code>pandas</code> dataframe that is interpretable as a CSV.</p>

<h2 id="returns">Returns</h2>

<ul>
<li><code>tuple</code> containing:
<ul>
<li><code>df_mean</code>: <code>pandas.DataFrame</code> containing mean predictions</li>
<li><code>df_std</code>: <code>pandas.DataFrame</code> containing standard deviation predictions</li>
</ul></li>
</ul>

<h2 id="example">Example</h2>

<p>Using a local file:</p>

<div class="pdoc-code codehilite">
<pre><span></span><code><span class="kn">import</span> <span class="nn">pandas</span> <span class="k">as</span> <span class="nn">pd</span>
<span class="kn">import</span> <span class="nn">twinlab</span> <span class="k">as</span> <span class="nn">tl</span>

<span class="n">df</span> <span class="o">=</span> <span class="n">pd</span><span class="o">.</span><span class="n">DataFrame</span><span class="p">({</span><span class="s1">&#39;X&#39;</span><span class="p">:</span> <span class="p">[</span><span class="mi">1</span><span class="p">,</span> <span class="mi">2</span><span class="p">,</span> <span class="mi">3</span><span class="p">,</span> <span class="mi">4</span><span class="p">],</span> <span class="s1">&#39;y&#39;</span><span class="p">:</span> <span class="p">[</span><span class="mi">1</span><span class="p">,</span> <span class="mi">4</span><span class="p">,</span> <span class="mi">9</span><span class="p">,</span> <span class="mi">16</span><span class="p">]})</span>
<span class="n">tl</span><span class="o">.</span><span class="n">upload_dataset</span><span class="p">(</span><span class="n">df</span><span class="p">,</span> <span class="s2">&quot;my_dataset&quot;</span><span class="p">)</span>
<span class="n">params</span> <span class="o">=</span> <span class="p">{</span>
    <span class="s2">&quot;dataset_id&quot;</span><span class="p">:</span> <span class="s2">&quot;my_dataset&quot;</span><span class="p">,</span>
    <span class="s2">&quot;inputs&quot;</span><span class="p">:</span> <span class="p">[</span><span class="s2">&quot;X&quot;</span><span class="p">],</span>
    <span class="s2">&quot;outputs&quot;</span><span class="p">:</span> <span class="p">[</span><span class="s2">&quot;y&quot;</span><span class="p">],</span>
<span class="p">}</span>
<span class="n">tl</span><span class="o">.</span><span class="n">train_campaign</span><span class="p">(</span><span class="n">params</span><span class="p">,</span> <span class="s2">&quot;my_campaign&quot;</span><span class="p">)</span>
<span class="n">filepath</span> <span class="o">=</span> <span class="s2">&quot;path/to/data.csv&quot;</span> <span class="c1"># Local</span>
<span class="n">campaign_id</span> <span class="o">=</span> <span class="s1">&#39;my_campaign&quot; # Pre-trained</span>
<span class="n">df_mean</span><span class="p">,</span> <span class="n">df_std</span> <span class="o">=</span> <span class="n">tl</span><span class="o">.</span><span class="n">predict_campaign</span><span class="p">(</span><span class="n">filepath</span><span class="p">,</span> <span class="n">campaign_id</span><span class="p">)</span>
<span class="nb">print</span><span class="p">(</span><span class="n">df_mean</span><span class="p">)</span>
<span class="nb">print</span><span class="p">(</span><span class="n">df_std</span><span class="p">)</span>
</code></pre>
</div>

<p>Using a <code>pandas</code> dataframe:</p>

<div class="pdoc-code codehilite">
<pre><span></span><code><span class="kn">import</span> <span class="nn">pandas</span> <span class="k">as</span> <span class="nn">pd</span>
<span class="kn">import</span> <span class="nn">twinlab</span> <span class="k">as</span> <span class="nn">tl</span>

<span class="n">df</span> <span class="o">=</span> <span class="n">pd</span><span class="o">.</span><span class="n">DataFrame</span><span class="p">({</span><span class="s1">&#39;X&#39;</span><span class="p">:</span> <span class="p">[</span><span class="mi">1</span><span class="p">,</span> <span class="mi">2</span><span class="p">,</span> <span class="mi">3</span><span class="p">,</span> <span class="mi">4</span><span class="p">],</span> <span class="s1">&#39;y&#39;</span><span class="p">:</span> <span class="p">[</span><span class="mi">1</span><span class="p">,</span> <span class="mi">4</span><span class="p">,</span> <span class="mi">9</span><span class="p">,</span> <span class="mi">16</span><span class="p">]})</span>
<span class="n">tl</span><span class="o">.</span><span class="n">upload_dataset</span><span class="p">(</span><span class="n">df</span><span class="p">,</span> <span class="s2">&quot;my_dataset&quot;</span><span class="p">)</span>
<span class="n">params</span> <span class="o">=</span> <span class="p">{</span>
    <span class="s2">&quot;dataset_id&quot;</span><span class="p">:</span> <span class="s2">&quot;my_dataset&quot;</span><span class="p">,</span>
    <span class="s2">&quot;inputs&quot;</span><span class="p">:</span> <span class="p">[</span><span class="s2">&quot;X&quot;</span><span class="p">],</span>
    <span class="s2">&quot;outputs&quot;</span><span class="p">:</span> <span class="p">[</span><span class="s2">&quot;y&quot;</span><span class="p">],</span>
<span class="p">}</span>
<span class="n">tl</span><span class="o">.</span><span class="n">train_campaign</span><span class="p">(</span><span class="n">params</span><span class="p">,</span> <span class="s2">&quot;my_campaign&quot;</span><span class="p">)</span>
<span class="n">df</span> <span class="o">=</span> <span class="n">pd</span><span class="o">.</span><span class="n">DataFrame</span><span class="p">({</span><span class="s1">&#39;X&#39;</span><span class="p">:</span> <span class="p">[</span><span class="mf">1.5</span><span class="p">,</span> <span class="mf">2.5</span><span class="p">,</span> <span class="mf">3.5</span><span class="p">]})</span>
<span class="n">tl</span><span class="o">.</span><span class="n">predict_campaign</span><span class="p">(</span><span class="n">df</span><span class="p">,</span> <span class="s2">&quot;my_campaign&quot;</span><span class="p">)</span>
</code></pre>
</div>
</div>


                </section>
                <section id="sample_campaign">
                            <input id="sample_campaign-view-source" class="view-source-toggle-state" type="checkbox" aria-hidden="true" tabindex="-1">
<div class="attr function">
            
        <span class="def">def</span>
        <span class="name">sample_campaign</span><span class="signature pdoc-code multiline">(<span class="param">	<span class="n">filepath_or_df</span><span class="p">:</span> <span class="n">Union</span><span class="p">[</span><span class="nb">str</span><span class="p">,</span> <span class="n">pandas</span><span class="o">.</span><span class="n">core</span><span class="o">.</span><span class="n">frame</span><span class="o">.</span><span class="n">DataFrame</span><span class="p">]</span>,</span><span class="param">	<span class="n">campaign_id</span><span class="p">:</span> <span class="nb">str</span>,</span><span class="param">	<span class="n">num_samples</span><span class="p">:</span> <span class="nb">int</span>,</span><span class="param">	<span class="n">processor</span><span class="p">:</span> <span class="n">Optional</span><span class="p">[</span><span class="nb">str</span><span class="p">]</span> <span class="o">=</span> <span class="s1">&#39;cpu&#39;</span>,</span><span class="param">	<span class="n">verbose</span><span class="p">:</span> <span class="n">Optional</span><span class="p">[</span><span class="nb">bool</span><span class="p">]</span> <span class="o">=</span> <span class="kc">False</span>,</span><span class="param">	<span class="n">debug</span><span class="p">:</span> <span class="n">Optional</span><span class="p">[</span><span class="nb">bool</span><span class="p">]</span> <span class="o">=</span> <span class="kc">False</span>,</span><span class="param">	<span class="o">**</span><span class="n">kwargs</span></span><span class="return-annotation">) -> <span class="n">pandas</span><span class="o">.</span><span class="n">core</span><span class="o">.</span><span class="n">frame</span><span class="o">.</span><span class="n">DataFrame</span>:</span></span>

                <label class="view-source-button" for="sample_campaign-view-source"><span>View Source</span></label>

    </div>
    <a class="headerlink" href="#sample_campaign"></a>
            <div class="pdoc-code codehilite"><pre><span></span><span id="sample_campaign-767"><a href="#sample_campaign-767"><span class="linenos">767</span></a><span class="k">def</span> <span class="nf">sample_campaign</span><span class="p">(</span>
</span><span id="sample_campaign-768"><a href="#sample_campaign-768"><span class="linenos">768</span></a>    <span class="n">filepath_or_df</span><span class="p">:</span> <span class="n">Union</span><span class="p">[</span><span class="nb">str</span><span class="p">,</span> <span class="n">pd</span><span class="o">.</span><span class="n">DataFrame</span><span class="p">],</span>
</span><span id="sample_campaign-769"><a href="#sample_campaign-769"><span class="linenos">769</span></a>    <span class="n">campaign_id</span><span class="p">:</span> <span class="nb">str</span><span class="p">,</span>
</span><span id="sample_campaign-770"><a href="#sample_campaign-770"><span class="linenos">770</span></a>    <span class="n">num_samples</span><span class="p">:</span> <span class="nb">int</span><span class="p">,</span>
</span><span id="sample_campaign-771"><a href="#sample_campaign-771"><span class="linenos">771</span></a>    <span class="n">processor</span><span class="p">:</span> <span class="n">Optional</span><span class="p">[</span><span class="nb">str</span><span class="p">]</span> <span class="o">=</span> <span class="s2">&quot;cpu&quot;</span><span class="p">,</span>
</span><span id="sample_campaign-772"><a href="#sample_campaign-772"><span class="linenos">772</span></a>    <span class="n">verbose</span><span class="p">:</span> <span class="n">Optional</span><span class="p">[</span><span class="nb">bool</span><span class="p">]</span> <span class="o">=</span> <span class="kc">False</span><span class="p">,</span>
</span><span id="sample_campaign-773"><a href="#sample_campaign-773"><span class="linenos">773</span></a>    <span class="n">debug</span><span class="p">:</span> <span class="n">Optional</span><span class="p">[</span><span class="nb">bool</span><span class="p">]</span> <span class="o">=</span> <span class="kc">False</span><span class="p">,</span>
</span><span id="sample_campaign-774"><a href="#sample_campaign-774"><span class="linenos">774</span></a>    <span class="o">**</span><span class="n">kwargs</span><span class="p">,</span>
</span><span id="sample_campaign-775"><a href="#sample_campaign-775"><span class="linenos">775</span></a><span class="p">)</span> <span class="o">-&gt;</span> <span class="n">pd</span><span class="o">.</span><span class="n">DataFrame</span><span class="p">:</span>
</span><span id="sample_campaign-776"><a href="#sample_campaign-776"><span class="linenos">776</span></a><span class="w">    </span><span class="sd">&quot;&quot;&quot;</span>
</span><span id="sample_campaign-777"><a href="#sample_campaign-777"><span class="linenos">777</span></a><span class="sd">    # Sample campaign</span>
</span><span id="sample_campaign-778"><a href="#sample_campaign-778"><span class="linenos">778</span></a>
</span><span id="sample_campaign-779"><a href="#sample_campaign-779"><span class="linenos">779</span></a><span class="sd">    Draw samples from a pre-trained campaign that exists on the `twinLab` cloud.</span>
</span><span id="sample_campaign-780"><a href="#sample_campaign-780"><span class="linenos">780</span></a>
</span><span id="sample_campaign-781"><a href="#sample_campaign-781"><span class="linenos">781</span></a><span class="sd">    ## Arguments</span>
</span><span id="sample_campaign-782"><a href="#sample_campaign-782"><span class="linenos">782</span></a>
</span><span id="sample_campaign-783"><a href="#sample_campaign-783"><span class="linenos">783</span></a><span class="sd">    - `filepath_or_df`: `str`; location of csv dataset on local machine for evaluation</span>
</span><span id="sample_campaign-784"><a href="#sample_campaign-784"><span class="linenos">784</span></a><span class="sd">        or `pandas` dataframe</span>
</span><span id="sample_campaign-785"><a href="#sample_campaign-785"><span class="linenos">785</span></a><span class="sd">    - `campaign_id`: `str`; name of pre-trained campaign to use for predictions</span>
</span><span id="sample_campaign-786"><a href="#sample_campaign-786"><span class="linenos">786</span></a><span class="sd">    - `num_samples`: `int`; number of samples to draw for each row of the evaluation data</span>
</span><span id="sample_campaign-787"><a href="#sample_campaign-787"><span class="linenos">787</span></a><span class="sd">    - `processor`: `str`, Optional, processor to use for sampling (&quot;cpu&quot;; &quot;gpu&quot;)</span>
</span><span id="sample_campaign-788"><a href="#sample_campaign-788"><span class="linenos">788</span></a><span class="sd">    - `verbose`: `bool`, Optional, determining level of information returned to the user</span>
</span><span id="sample_campaign-789"><a href="#sample_campaign-789"><span class="linenos">789</span></a><span class="sd">    - `debug`: `bool`, Optional, determining level of information logged on the server</span>
</span><span id="sample_campaign-790"><a href="#sample_campaign-790"><span class="linenos">790</span></a>
</span><span id="sample_campaign-791"><a href="#sample_campaign-791"><span class="linenos">791</span></a><span class="sd">    **NOTE:** Evaluation data must be a CSV file, or a `pandas` dataframe that is interpretable as a CSV.</span>
</span><span id="sample_campaign-792"><a href="#sample_campaign-792"><span class="linenos">792</span></a>
</span><span id="sample_campaign-793"><a href="#sample_campaign-793"><span class="linenos">793</span></a><span class="sd">    ## Returns</span>
</span><span id="sample_campaign-794"><a href="#sample_campaign-794"><span class="linenos">794</span></a>
</span><span id="sample_campaign-795"><a href="#sample_campaign-795"><span class="linenos">795</span></a><span class="sd">    - `DataFrame` with the sampled values</span>
</span><span id="sample_campaign-796"><a href="#sample_campaign-796"><span class="linenos">796</span></a>
</span><span id="sample_campaign-797"><a href="#sample_campaign-797"><span class="linenos">797</span></a><span class="sd">    ## Example</span>
</span><span id="sample_campaign-798"><a href="#sample_campaign-798"><span class="linenos">798</span></a>
</span><span id="sample_campaign-799"><a href="#sample_campaign-799"><span class="linenos">799</span></a><span class="sd">    Using a local file:</span>
</span><span id="sample_campaign-800"><a href="#sample_campaign-800"><span class="linenos">800</span></a><span class="sd">    ```python</span>
</span><span id="sample_campaign-801"><a href="#sample_campaign-801"><span class="linenos">801</span></a><span class="sd">    import pandas as pd</span>
</span><span id="sample_campaign-802"><a href="#sample_campaign-802"><span class="linenos">802</span></a><span class="sd">    import twinlab as tl</span>
</span><span id="sample_campaign-803"><a href="#sample_campaign-803"><span class="linenos">803</span></a>
</span><span id="sample_campaign-804"><a href="#sample_campaign-804"><span class="linenos">804</span></a><span class="sd">    df = pd.DataFrame({&#39;X&#39;: [1, 2, 3, 4], &#39;y&#39;: [1, 4, 9, 16]})</span>
</span><span id="sample_campaign-805"><a href="#sample_campaign-805"><span class="linenos">805</span></a><span class="sd">    tl.upload_dataset(df, &quot;my_dataset&quot;)</span>
</span><span id="sample_campaign-806"><a href="#sample_campaign-806"><span class="linenos">806</span></a><span class="sd">    params = {</span>
</span><span id="sample_campaign-807"><a href="#sample_campaign-807"><span class="linenos">807</span></a><span class="sd">        &quot;dataset_id&quot;: &quot;my_dataset&quot;,</span>
</span><span id="sample_campaign-808"><a href="#sample_campaign-808"><span class="linenos">808</span></a><span class="sd">        &quot;inputs&quot;: [&quot;X&quot;],</span>
</span><span id="sample_campaign-809"><a href="#sample_campaign-809"><span class="linenos">809</span></a><span class="sd">        &quot;outputs&quot;: [&quot;y&quot;],</span>
</span><span id="sample_campaign-810"><a href="#sample_campaign-810"><span class="linenos">810</span></a><span class="sd">    }</span>
</span><span id="sample_campaign-811"><a href="#sample_campaign-811"><span class="linenos">811</span></a><span class="sd">    tl.train_campaign(params, &quot;my_campaign&quot;)</span>
</span><span id="sample_campaign-812"><a href="#sample_campaign-812"><span class="linenos">812</span></a><span class="sd">    filepath = &quot;path/to/data.csv&quot; # Local</span>
</span><span id="sample_campaign-813"><a href="#sample_campaign-813"><span class="linenos">813</span></a><span class="sd">    n = 10</span>
</span><span id="sample_campaign-814"><a href="#sample_campaign-814"><span class="linenos">814</span></a><span class="sd">    df_mean, df_std = tl.sample_campaign(filepath, &quot;my_campaign&quot;, n)</span>
</span><span id="sample_campaign-815"><a href="#sample_campaign-815"><span class="linenos">815</span></a><span class="sd">    print(df_mean)</span>
</span><span id="sample_campaign-816"><a href="#sample_campaign-816"><span class="linenos">816</span></a><span class="sd">    print(df_std)</span>
</span><span id="sample_campaign-817"><a href="#sample_campaign-817"><span class="linenos">817</span></a><span class="sd">    ```</span>
</span><span id="sample_campaign-818"><a href="#sample_campaign-818"><span class="linenos">818</span></a>
</span><span id="sample_campaign-819"><a href="#sample_campaign-819"><span class="linenos">819</span></a><span class="sd">    Using a `pandas` dataframe:</span>
</span><span id="sample_campaign-820"><a href="#sample_campaign-820"><span class="linenos">820</span></a><span class="sd">    ```python</span>
</span><span id="sample_campaign-821"><a href="#sample_campaign-821"><span class="linenos">821</span></a><span class="sd">    import pandas as pd</span>
</span><span id="sample_campaign-822"><a href="#sample_campaign-822"><span class="linenos">822</span></a><span class="sd">    import twinlab as tl</span>
</span><span id="sample_campaign-823"><a href="#sample_campaign-823"><span class="linenos">823</span></a>
</span><span id="sample_campaign-824"><a href="#sample_campaign-824"><span class="linenos">824</span></a><span class="sd">    df = pd.DataFrame({&#39;X&#39;: [1, 2, 3, 4], &#39;y&#39;: [1, 4, 9, 16]})</span>
</span><span id="sample_campaign-825"><a href="#sample_campaign-825"><span class="linenos">825</span></a><span class="sd">    tl.upload_dataset(df, &quot;my_dataset&quot;)</span>
</span><span id="sample_campaign-826"><a href="#sample_campaign-826"><span class="linenos">826</span></a><span class="sd">    params = {</span>
</span><span id="sample_campaign-827"><a href="#sample_campaign-827"><span class="linenos">827</span></a><span class="sd">        &quot;dataset_id&quot;: &quot;my_dataset&quot;,</span>
</span><span id="sample_campaign-828"><a href="#sample_campaign-828"><span class="linenos">828</span></a><span class="sd">        &quot;inputs&quot;: [&quot;X&quot;],</span>
</span><span id="sample_campaign-829"><a href="#sample_campaign-829"><span class="linenos">829</span></a><span class="sd">        &quot;outputs&quot;: [&quot;y&quot;],</span>
</span><span id="sample_campaign-830"><a href="#sample_campaign-830"><span class="linenos">830</span></a><span class="sd">    }</span>
</span><span id="sample_campaign-831"><a href="#sample_campaign-831"><span class="linenos">831</span></a><span class="sd">    tl.train_campaign(params, &quot;my_campaign&quot;)</span>
</span><span id="sample_campaign-832"><a href="#sample_campaign-832"><span class="linenos">832</span></a><span class="sd">    df = pd.DataFrame({&#39;X&#39;: [1.5, 2.5, 3.5]})</span>
</span><span id="sample_campaign-833"><a href="#sample_campaign-833"><span class="linenos">833</span></a><span class="sd">    n = 10</span>
</span><span id="sample_campaign-834"><a href="#sample_campaign-834"><span class="linenos">834</span></a><span class="sd">    tl.sample_campaign(df, &quot;my_campaign&quot;, n)</span>
</span><span id="sample_campaign-835"><a href="#sample_campaign-835"><span class="linenos">835</span></a><span class="sd">    ```</span>
</span><span id="sample_campaign-836"><a href="#sample_campaign-836"><span class="linenos">836</span></a><span class="sd">    &quot;&quot;&quot;</span>
</span><span id="sample_campaign-837"><a href="#sample_campaign-837"><span class="linenos">837</span></a>
</span><span id="sample_campaign-838"><a href="#sample_campaign-838"><span class="linenos">838</span></a>    <span class="n">csv</span> <span class="o">=</span> <span class="n">_use_campaign</span><span class="p">(</span>
</span><span id="sample_campaign-839"><a href="#sample_campaign-839"><span class="linenos">839</span></a>        <span class="n">campaign_id</span><span class="p">,</span>
</span><span id="sample_campaign-840"><a href="#sample_campaign-840"><span class="linenos">840</span></a>        <span class="n">method</span><span class="o">=</span><span class="s2">&quot;sample&quot;</span><span class="p">,</span>
</span><span id="sample_campaign-841"><a href="#sample_campaign-841"><span class="linenos">841</span></a>        <span class="n">filepath_or_df</span><span class="o">=</span><span class="n">filepath_or_df</span><span class="p">,</span>
</span><span id="sample_campaign-842"><a href="#sample_campaign-842"><span class="linenos">842</span></a>        <span class="n">num_samples</span><span class="o">=</span><span class="n">num_samples</span><span class="p">,</span>
</span><span id="sample_campaign-843"><a href="#sample_campaign-843"><span class="linenos">843</span></a>        <span class="n">processor</span><span class="o">=</span><span class="n">processor</span><span class="p">,</span>
</span><span id="sample_campaign-844"><a href="#sample_campaign-844"><span class="linenos">844</span></a>        <span class="n">verbose</span><span class="o">=</span><span class="n">verbose</span><span class="p">,</span>
</span><span id="sample_campaign-845"><a href="#sample_campaign-845"><span class="linenos">845</span></a>        <span class="n">debug</span><span class="o">=</span><span class="n">debug</span><span class="p">,</span>
</span><span id="sample_campaign-846"><a href="#sample_campaign-846"><span class="linenos">846</span></a>        <span class="o">**</span><span class="n">kwargs</span><span class="p">,</span>
</span><span id="sample_campaign-847"><a href="#sample_campaign-847"><span class="linenos">847</span></a>    <span class="p">)</span>
</span><span id="sample_campaign-848"><a href="#sample_campaign-848"><span class="linenos">848</span></a>    <span class="n">df</span> <span class="o">=</span> <span class="n">pd</span><span class="o">.</span><span class="n">read_csv</span><span class="p">(</span><span class="n">csv</span><span class="p">,</span> <span class="n">header</span><span class="o">=</span><span class="p">[</span><span class="mi">0</span><span class="p">,</span> <span class="mi">1</span><span class="p">],</span> <span class="n">sep</span><span class="o">=</span><span class="s2">&quot;,&quot;</span><span class="p">)</span>
</span><span id="sample_campaign-849"><a href="#sample_campaign-849"><span class="linenos">849</span></a>    <span class="k">if</span> <span class="n">verbose</span><span class="p">:</span>
</span><span id="sample_campaign-850"><a href="#sample_campaign-850"><span class="linenos">850</span></a>        <span class="nb">print</span><span class="p">(</span><span class="s2">&quot;Samples:&quot;</span><span class="p">)</span>
</span><span id="sample_campaign-851"><a href="#sample_campaign-851"><span class="linenos">851</span></a>        <span class="nb">print</span><span class="p">(</span><span class="n">df</span><span class="p">)</span>
</span><span id="sample_campaign-852"><a href="#sample_campaign-852"><span class="linenos">852</span></a>    <span class="k">return</span> <span class="n">df</span>
</span></pre></div>


            <div class="docstring"><h1 id="sample-campaign">Sample campaign</h1>

<p>Draw samples from a pre-trained campaign that exists on the <code>twinLab</code> cloud.</p>

<h2 id="arguments">Arguments</h2>

<ul>
<li><code>filepath_or_df</code>: <code>str</code>; location of csv dataset on local machine for evaluation
or <code>pandas</code> dataframe</li>
<li><code>campaign_id</code>: <code>str</code>; name of pre-trained campaign to use for predictions</li>
<li><code>num_samples</code>: <code>int</code>; number of samples to draw for each row of the evaluation data</li>
<li><code>processor</code>: <code>str</code>, Optional, processor to use for sampling ("cpu"; "gpu")</li>
<li><code>verbose</code>: <code>bool</code>, Optional, determining level of information returned to the user</li>
<li><code>debug</code>: <code>bool</code>, Optional, determining level of information logged on the server</li>
</ul>

<p><strong>NOTE:</strong> Evaluation data must be a CSV file, or a <code>pandas</code> dataframe that is interpretable as a CSV.</p>

<h2 id="returns">Returns</h2>

<ul>
<li><code>DataFrame</code> with the sampled values</li>
</ul>

<h2 id="example">Example</h2>

<p>Using a local file:</p>

<div class="pdoc-code codehilite">
<pre><span></span><code><span class="kn">import</span> <span class="nn">pandas</span> <span class="k">as</span> <span class="nn">pd</span>
<span class="kn">import</span> <span class="nn">twinlab</span> <span class="k">as</span> <span class="nn">tl</span>

<span class="n">df</span> <span class="o">=</span> <span class="n">pd</span><span class="o">.</span><span class="n">DataFrame</span><span class="p">({</span><span class="s1">&#39;X&#39;</span><span class="p">:</span> <span class="p">[</span><span class="mi">1</span><span class="p">,</span> <span class="mi">2</span><span class="p">,</span> <span class="mi">3</span><span class="p">,</span> <span class="mi">4</span><span class="p">],</span> <span class="s1">&#39;y&#39;</span><span class="p">:</span> <span class="p">[</span><span class="mi">1</span><span class="p">,</span> <span class="mi">4</span><span class="p">,</span> <span class="mi">9</span><span class="p">,</span> <span class="mi">16</span><span class="p">]})</span>
<span class="n">tl</span><span class="o">.</span><span class="n">upload_dataset</span><span class="p">(</span><span class="n">df</span><span class="p">,</span> <span class="s2">&quot;my_dataset&quot;</span><span class="p">)</span>
<span class="n">params</span> <span class="o">=</span> <span class="p">{</span>
    <span class="s2">&quot;dataset_id&quot;</span><span class="p">:</span> <span class="s2">&quot;my_dataset&quot;</span><span class="p">,</span>
    <span class="s2">&quot;inputs&quot;</span><span class="p">:</span> <span class="p">[</span><span class="s2">&quot;X&quot;</span><span class="p">],</span>
    <span class="s2">&quot;outputs&quot;</span><span class="p">:</span> <span class="p">[</span><span class="s2">&quot;y&quot;</span><span class="p">],</span>
<span class="p">}</span>
<span class="n">tl</span><span class="o">.</span><span class="n">train_campaign</span><span class="p">(</span><span class="n">params</span><span class="p">,</span> <span class="s2">&quot;my_campaign&quot;</span><span class="p">)</span>
<span class="n">filepath</span> <span class="o">=</span> <span class="s2">&quot;path/to/data.csv&quot;</span> <span class="c1"># Local</span>
<span class="n">n</span> <span class="o">=</span> <span class="mi">10</span>
<span class="n">df_mean</span><span class="p">,</span> <span class="n">df_std</span> <span class="o">=</span> <span class="n">tl</span><span class="o">.</span><span class="n">sample_campaign</span><span class="p">(</span><span class="n">filepath</span><span class="p">,</span> <span class="s2">&quot;my_campaign&quot;</span><span class="p">,</span> <span class="n">n</span><span class="p">)</span>
<span class="nb">print</span><span class="p">(</span><span class="n">df_mean</span><span class="p">)</span>
<span class="nb">print</span><span class="p">(</span><span class="n">df_std</span><span class="p">)</span>
</code></pre>
</div>

<p>Using a <code>pandas</code> dataframe:</p>

<div class="pdoc-code codehilite">
<pre><span></span><code><span class="kn">import</span> <span class="nn">pandas</span> <span class="k">as</span> <span class="nn">pd</span>
<span class="kn">import</span> <span class="nn">twinlab</span> <span class="k">as</span> <span class="nn">tl</span>

<span class="n">df</span> <span class="o">=</span> <span class="n">pd</span><span class="o">.</span><span class="n">DataFrame</span><span class="p">({</span><span class="s1">&#39;X&#39;</span><span class="p">:</span> <span class="p">[</span><span class="mi">1</span><span class="p">,</span> <span class="mi">2</span><span class="p">,</span> <span class="mi">3</span><span class="p">,</span> <span class="mi">4</span><span class="p">],</span> <span class="s1">&#39;y&#39;</span><span class="p">:</span> <span class="p">[</span><span class="mi">1</span><span class="p">,</span> <span class="mi">4</span><span class="p">,</span> <span class="mi">9</span><span class="p">,</span> <span class="mi">16</span><span class="p">]})</span>
<span class="n">tl</span><span class="o">.</span><span class="n">upload_dataset</span><span class="p">(</span><span class="n">df</span><span class="p">,</span> <span class="s2">&quot;my_dataset&quot;</span><span class="p">)</span>
<span class="n">params</span> <span class="o">=</span> <span class="p">{</span>
    <span class="s2">&quot;dataset_id&quot;</span><span class="p">:</span> <span class="s2">&quot;my_dataset&quot;</span><span class="p">,</span>
    <span class="s2">&quot;inputs&quot;</span><span class="p">:</span> <span class="p">[</span><span class="s2">&quot;X&quot;</span><span class="p">],</span>
    <span class="s2">&quot;outputs&quot;</span><span class="p">:</span> <span class="p">[</span><span class="s2">&quot;y&quot;</span><span class="p">],</span>
<span class="p">}</span>
<span class="n">tl</span><span class="o">.</span><span class="n">train_campaign</span><span class="p">(</span><span class="n">params</span><span class="p">,</span> <span class="s2">&quot;my_campaign&quot;</span><span class="p">)</span>
<span class="n">df</span> <span class="o">=</span> <span class="n">pd</span><span class="o">.</span><span class="n">DataFrame</span><span class="p">({</span><span class="s1">&#39;X&#39;</span><span class="p">:</span> <span class="p">[</span><span class="mf">1.5</span><span class="p">,</span> <span class="mf">2.5</span><span class="p">,</span> <span class="mf">3.5</span><span class="p">]})</span>
<span class="n">n</span> <span class="o">=</span> <span class="mi">10</span>
<span class="n">tl</span><span class="o">.</span><span class="n">sample_campaign</span><span class="p">(</span><span class="n">df</span><span class="p">,</span> <span class="s2">&quot;my_campaign&quot;</span><span class="p">,</span> <span class="n">n</span><span class="p">)</span>
</code></pre>
</div>
</div>


                </section>
                <section id="active_learn_campaign">
                            <input id="active_learn_campaign-view-source" class="view-source-toggle-state" type="checkbox" aria-hidden="true" tabindex="-1">
<div class="attr function">
            
        <span class="def">def</span>
        <span class="name">active_learn_campaign</span><span class="signature pdoc-code multiline">(<span class="param">	<span class="n">campaign_id</span><span class="p">:</span> <span class="nb">str</span>,</span><span class="param">	<span class="n">num_points</span><span class="p">:</span> <span class="nb">int</span>,</span><span class="param">	<span class="n">processor</span><span class="p">:</span> <span class="n">Optional</span><span class="p">[</span><span class="nb">str</span><span class="p">]</span> <span class="o">=</span> <span class="s1">&#39;cpu&#39;</span>,</span><span class="param">	<span class="n">verbose</span><span class="p">:</span> <span class="n">Optional</span><span class="p">[</span><span class="nb">bool</span><span class="p">]</span> <span class="o">=</span> <span class="kc">False</span>,</span><span class="param">	<span class="n">debug</span><span class="p">:</span> <span class="n">Optional</span><span class="p">[</span><span class="nb">bool</span><span class="p">]</span> <span class="o">=</span> <span class="kc">False</span>,</span><span class="param">	<span class="o">**</span><span class="n">kwargs</span></span><span class="return-annotation">) -> <span class="n">pandas</span><span class="o">.</span><span class="n">core</span><span class="o">.</span><span class="n">frame</span><span class="o">.</span><span class="n">DataFrame</span>:</span></span>

                <label class="view-source-button" for="active_learn_campaign-view-source"><span>View Source</span></label>

    </div>
    <a class="headerlink" href="#active_learn_campaign"></a>
            <div class="pdoc-code codehilite"><pre><span></span><span id="active_learn_campaign-856"><a href="#active_learn_campaign-856"><span class="linenos">856</span></a><span class="k">def</span> <span class="nf">active_learn_campaign</span><span class="p">(</span>
</span><span id="active_learn_campaign-857"><a href="#active_learn_campaign-857"><span class="linenos">857</span></a>    <span class="n">campaign_id</span><span class="p">:</span> <span class="nb">str</span><span class="p">,</span>
</span><span id="active_learn_campaign-858"><a href="#active_learn_campaign-858"><span class="linenos">858</span></a>    <span class="n">num_points</span><span class="p">:</span> <span class="nb">int</span><span class="p">,</span>
</span><span id="active_learn_campaign-859"><a href="#active_learn_campaign-859"><span class="linenos">859</span></a>    <span class="n">processor</span><span class="p">:</span> <span class="n">Optional</span><span class="p">[</span><span class="nb">str</span><span class="p">]</span> <span class="o">=</span> <span class="s2">&quot;cpu&quot;</span><span class="p">,</span>
</span><span id="active_learn_campaign-860"><a href="#active_learn_campaign-860"><span class="linenos">860</span></a>    <span class="n">verbose</span><span class="p">:</span> <span class="n">Optional</span><span class="p">[</span><span class="nb">bool</span><span class="p">]</span> <span class="o">=</span> <span class="kc">False</span><span class="p">,</span>
</span><span id="active_learn_campaign-861"><a href="#active_learn_campaign-861"><span class="linenos">861</span></a>    <span class="n">debug</span><span class="p">:</span> <span class="n">Optional</span><span class="p">[</span><span class="nb">bool</span><span class="p">]</span> <span class="o">=</span> <span class="kc">False</span><span class="p">,</span>
</span><span id="active_learn_campaign-862"><a href="#active_learn_campaign-862"><span class="linenos">862</span></a>    <span class="o">**</span><span class="n">kwargs</span><span class="p">,</span>
</span><span id="active_learn_campaign-863"><a href="#active_learn_campaign-863"><span class="linenos">863</span></a><span class="p">)</span> <span class="o">-&gt;</span> <span class="n">pd</span><span class="o">.</span><span class="n">DataFrame</span><span class="p">:</span>
</span><span id="active_learn_campaign-864"><a href="#active_learn_campaign-864"><span class="linenos">864</span></a><span class="w">    </span><span class="sd">&quot;&quot;&quot;</span>
</span><span id="active_learn_campaign-865"><a href="#active_learn_campaign-865"><span class="linenos">865</span></a><span class="sd">    # Active learn campaign</span>
</span><span id="active_learn_campaign-866"><a href="#active_learn_campaign-866"><span class="linenos">866</span></a>
</span><span id="active_learn_campaign-867"><a href="#active_learn_campaign-867"><span class="linenos">867</span></a><span class="sd">    Draw new candidate data points via active learning from a pre-trained campaign</span>
</span><span id="active_learn_campaign-868"><a href="#active_learn_campaign-868"><span class="linenos">868</span></a><span class="sd">    that exists on the `twinLab` cloud.</span>
</span><span id="active_learn_campaign-869"><a href="#active_learn_campaign-869"><span class="linenos">869</span></a>
</span><span id="active_learn_campaign-870"><a href="#active_learn_campaign-870"><span class="linenos">870</span></a><span class="sd">    ## Arguments</span>
</span><span id="active_learn_campaign-871"><a href="#active_learn_campaign-871"><span class="linenos">871</span></a><span class="sd">    - `campaign_id`: `str`; name of pre-trained campaign to use for predictions</span>
</span><span id="active_learn_campaign-872"><a href="#active_learn_campaign-872"><span class="linenos">872</span></a><span class="sd">    - `num_points`: `int`; number of samples to draw for each row of the evaluation data</span>
</span><span id="active_learn_campaign-873"><a href="#active_learn_campaign-873"><span class="linenos">873</span></a><span class="sd">    - `processor`: `str`, Optional, processor to use for sampling (&quot;cpu&quot;; &quot;gpu&quot;)</span>
</span><span id="active_learn_campaign-874"><a href="#active_learn_campaign-874"><span class="linenos">874</span></a><span class="sd">    - `verbose`: `bool`, Optional, determining level of information returned to the user</span>
</span><span id="active_learn_campaign-875"><a href="#active_learn_campaign-875"><span class="linenos">875</span></a><span class="sd">    - `debug`: `bool`, Optional, determining level of information logged on the server</span>
</span><span id="active_learn_campaign-876"><a href="#active_learn_campaign-876"><span class="linenos">876</span></a>
</span><span id="active_learn_campaign-877"><a href="#active_learn_campaign-877"><span class="linenos">877</span></a><span class="sd">    ## Returns</span>
</span><span id="active_learn_campaign-878"><a href="#active_learn_campaign-878"><span class="linenos">878</span></a>
</span><span id="active_learn_campaign-879"><a href="#active_learn_campaign-879"><span class="linenos">879</span></a><span class="sd">    - `Dataframe` containing the recommended sample locations</span>
</span><span id="active_learn_campaign-880"><a href="#active_learn_campaign-880"><span class="linenos">880</span></a>
</span><span id="active_learn_campaign-881"><a href="#active_learn_campaign-881"><span class="linenos">881</span></a><span class="sd">    ## Example</span>
</span><span id="active_learn_campaign-882"><a href="#active_learn_campaign-882"><span class="linenos">882</span></a>
</span><span id="active_learn_campaign-883"><a href="#active_learn_campaign-883"><span class="linenos">883</span></a><span class="sd">    ```python</span>
</span><span id="active_learn_campaign-884"><a href="#active_learn_campaign-884"><span class="linenos">884</span></a><span class="sd">    import pandas as pd</span>
</span><span id="active_learn_campaign-885"><a href="#active_learn_campaign-885"><span class="linenos">885</span></a><span class="sd">    import twinlab as tl</span>
</span><span id="active_learn_campaign-886"><a href="#active_learn_campaign-886"><span class="linenos">886</span></a>
</span><span id="active_learn_campaign-887"><a href="#active_learn_campaign-887"><span class="linenos">887</span></a><span class="sd">    df = pd.DataFrame({&#39;X&#39;: [1, 2, 3, 4], &#39;y&#39;: [1, 4, 9, 16]})</span>
</span><span id="active_learn_campaign-888"><a href="#active_learn_campaign-888"><span class="linenos">888</span></a><span class="sd">    tl.upload_dataset(df, &quot;my_dataset&quot;)</span>
</span><span id="active_learn_campaign-889"><a href="#active_learn_campaign-889"><span class="linenos">889</span></a><span class="sd">    params = {</span>
</span><span id="active_learn_campaign-890"><a href="#active_learn_campaign-890"><span class="linenos">890</span></a><span class="sd">        &quot;dataset_id&quot;: &quot;my_dataset&quot;,</span>
</span><span id="active_learn_campaign-891"><a href="#active_learn_campaign-891"><span class="linenos">891</span></a><span class="sd">        &quot;inputs&quot;: [&quot;X&quot;],</span>
</span><span id="active_learn_campaign-892"><a href="#active_learn_campaign-892"><span class="linenos">892</span></a><span class="sd">        &quot;outputs&quot;: [&quot;y&quot;],</span>
</span><span id="active_learn_campaign-893"><a href="#active_learn_campaign-893"><span class="linenos">893</span></a><span class="sd">    }</span>
</span><span id="active_learn_campaign-894"><a href="#active_learn_campaign-894"><span class="linenos">894</span></a><span class="sd">    tl.train_campaign(params, &quot;my_campaign&quot;)</span>
</span><span id="active_learn_campaign-895"><a href="#active_learn_campaign-895"><span class="linenos">895</span></a><span class="sd">    n = 10</span>
</span><span id="active_learn_campaign-896"><a href="#active_learn_campaign-896"><span class="linenos">896</span></a><span class="sd">    df = tl.active_learn_campaign(&quot;my_campaign&quot;, n)</span>
</span><span id="active_learn_campaign-897"><a href="#active_learn_campaign-897"><span class="linenos">897</span></a><span class="sd">    print(df)</span>
</span><span id="active_learn_campaign-898"><a href="#active_learn_campaign-898"><span class="linenos">898</span></a><span class="sd">    ```</span>
</span><span id="active_learn_campaign-899"><a href="#active_learn_campaign-899"><span class="linenos">899</span></a><span class="sd">    &quot;&quot;&quot;</span>
</span><span id="active_learn_campaign-900"><a href="#active_learn_campaign-900"><span class="linenos">900</span></a>
</span><span id="active_learn_campaign-901"><a href="#active_learn_campaign-901"><span class="linenos">901</span></a>    <span class="n">csv</span> <span class="o">=</span> <span class="n">_use_campaign</span><span class="p">(</span>
</span><span id="active_learn_campaign-902"><a href="#active_learn_campaign-902"><span class="linenos">902</span></a>        <span class="n">campaign_id</span><span class="p">,</span>
</span><span id="active_learn_campaign-903"><a href="#active_learn_campaign-903"><span class="linenos">903</span></a>        <span class="n">method</span><span class="o">=</span><span class="s2">&quot;get_candidate_points&quot;</span><span class="p">,</span>
</span><span id="active_learn_campaign-904"><a href="#active_learn_campaign-904"><span class="linenos">904</span></a>        <span class="n">acq_func</span><span class="o">=</span><span class="s2">&quot;qNIPV&quot;</span><span class="p">,</span>
</span><span id="active_learn_campaign-905"><a href="#active_learn_campaign-905"><span class="linenos">905</span></a>        <span class="n">num_points</span><span class="o">=</span><span class="n">num_points</span><span class="p">,</span>
</span><span id="active_learn_campaign-906"><a href="#active_learn_campaign-906"><span class="linenos">906</span></a>        <span class="n">processor</span><span class="o">=</span><span class="n">processor</span><span class="p">,</span>
</span><span id="active_learn_campaign-907"><a href="#active_learn_campaign-907"><span class="linenos">907</span></a>        <span class="n">verbose</span><span class="o">=</span><span class="n">verbose</span><span class="p">,</span>
</span><span id="active_learn_campaign-908"><a href="#active_learn_campaign-908"><span class="linenos">908</span></a>        <span class="n">debug</span><span class="o">=</span><span class="n">debug</span><span class="p">,</span>
</span><span id="active_learn_campaign-909"><a href="#active_learn_campaign-909"><span class="linenos">909</span></a>        <span class="o">**</span><span class="n">kwargs</span><span class="p">,</span>
</span><span id="active_learn_campaign-910"><a href="#active_learn_campaign-910"><span class="linenos">910</span></a>    <span class="p">)</span>
</span><span id="active_learn_campaign-911"><a href="#active_learn_campaign-911"><span class="linenos">911</span></a>    <span class="n">df</span> <span class="o">=</span> <span class="n">pd</span><span class="o">.</span><span class="n">read_csv</span><span class="p">(</span><span class="n">csv</span><span class="p">,</span> <span class="n">sep</span><span class="o">=</span><span class="s2">&quot;,&quot;</span><span class="p">)</span>
</span><span id="active_learn_campaign-912"><a href="#active_learn_campaign-912"><span class="linenos">912</span></a>    <span class="k">if</span> <span class="n">verbose</span><span class="p">:</span>
</span><span id="active_learn_campaign-913"><a href="#active_learn_campaign-913"><span class="linenos">913</span></a>        <span class="nb">print</span><span class="p">(</span><span class="s2">&quot;Candidate points:&quot;</span><span class="p">)</span>
</span><span id="active_learn_campaign-914"><a href="#active_learn_campaign-914"><span class="linenos">914</span></a>        <span class="nb">print</span><span class="p">(</span><span class="n">df</span><span class="p">)</span>
</span><span id="active_learn_campaign-915"><a href="#active_learn_campaign-915"><span class="linenos">915</span></a>    <span class="k">return</span> <span class="n">df</span>
</span></pre></div>


            <div class="docstring"><h1 id="active-learn-campaign">Active learn campaign</h1>

<p>Draw new candidate data points via active learning from a pre-trained campaign
that exists on the <code>twinLab</code> cloud.</p>

<h2 id="arguments">Arguments</h2>

<ul>
<li><code>campaign_id</code>: <code>str</code>; name of pre-trained campaign to use for predictions</li>
<li><code>num_points</code>: <code>int</code>; number of samples to draw for each row of the evaluation data</li>
<li><code>processor</code>: <code>str</code>, Optional, processor to use for sampling ("cpu"; "gpu")</li>
<li><code>verbose</code>: <code>bool</code>, Optional, determining level of information returned to the user</li>
<li><code>debug</code>: <code>bool</code>, Optional, determining level of information logged on the server</li>
</ul>

<h2 id="returns">Returns</h2>

<ul>
<li><code>Dataframe</code> containing the recommended sample locations</li>
</ul>

<h2 id="example">Example</h2>

<div class="pdoc-code codehilite">
<pre><span></span><code><span class="kn">import</span> <span class="nn">pandas</span> <span class="k">as</span> <span class="nn">pd</span>
<span class="kn">import</span> <span class="nn">twinlab</span> <span class="k">as</span> <span class="nn">tl</span>

<span class="n">df</span> <span class="o">=</span> <span class="n">pd</span><span class="o">.</span><span class="n">DataFrame</span><span class="p">({</span><span class="s1">&#39;X&#39;</span><span class="p">:</span> <span class="p">[</span><span class="mi">1</span><span class="p">,</span> <span class="mi">2</span><span class="p">,</span> <span class="mi">3</span><span class="p">,</span> <span class="mi">4</span><span class="p">],</span> <span class="s1">&#39;y&#39;</span><span class="p">:</span> <span class="p">[</span><span class="mi">1</span><span class="p">,</span> <span class="mi">4</span><span class="p">,</span> <span class="mi">9</span><span class="p">,</span> <span class="mi">16</span><span class="p">]})</span>
<span class="n">tl</span><span class="o">.</span><span class="n">upload_dataset</span><span class="p">(</span><span class="n">df</span><span class="p">,</span> <span class="s2">&quot;my_dataset&quot;</span><span class="p">)</span>
<span class="n">params</span> <span class="o">=</span> <span class="p">{</span>
    <span class="s2">&quot;dataset_id&quot;</span><span class="p">:</span> <span class="s2">&quot;my_dataset&quot;</span><span class="p">,</span>
    <span class="s2">&quot;inputs&quot;</span><span class="p">:</span> <span class="p">[</span><span class="s2">&quot;X&quot;</span><span class="p">],</span>
    <span class="s2">&quot;outputs&quot;</span><span class="p">:</span> <span class="p">[</span><span class="s2">&quot;y&quot;</span><span class="p">],</span>
<span class="p">}</span>
<span class="n">tl</span><span class="o">.</span><span class="n">train_campaign</span><span class="p">(</span><span class="n">params</span><span class="p">,</span> <span class="s2">&quot;my_campaign&quot;</span><span class="p">)</span>
<span class="n">n</span> <span class="o">=</span> <span class="mi">10</span>
<span class="n">df</span> <span class="o">=</span> <span class="n">tl</span><span class="o">.</span><span class="n">active_learn_campaign</span><span class="p">(</span><span class="s2">&quot;my_campaign&quot;</span><span class="p">,</span> <span class="n">n</span><span class="p">)</span>
<span class="nb">print</span><span class="p">(</span><span class="n">df</span><span class="p">)</span>
</code></pre>
</div>
</div>


                </section>
                <section id="optimise_campaign">
                            <input id="optimise_campaign-view-source" class="view-source-toggle-state" type="checkbox" aria-hidden="true" tabindex="-1">
<div class="attr function">
            
        <span class="def">def</span>
        <span class="name">optimise_campaign</span><span class="signature pdoc-code multiline">(<span class="param">	<span class="n">campaign_id</span><span class="p">:</span> <span class="nb">str</span>,</span><span class="param">	<span class="n">num_points</span><span class="p">:</span> <span class="nb">int</span>,</span><span class="param">	<span class="n">processor</span><span class="p">:</span> <span class="n">Optional</span><span class="p">[</span><span class="nb">str</span><span class="p">]</span> <span class="o">=</span> <span class="s1">&#39;cpu&#39;</span>,</span><span class="param">	<span class="n">verbose</span><span class="p">:</span> <span class="n">Optional</span><span class="p">[</span><span class="nb">bool</span><span class="p">]</span> <span class="o">=</span> <span class="kc">False</span>,</span><span class="param">	<span class="n">debug</span><span class="p">:</span> <span class="n">Optional</span><span class="p">[</span><span class="nb">bool</span><span class="p">]</span> <span class="o">=</span> <span class="kc">False</span>,</span><span class="param">	<span class="o">**</span><span class="n">kwargs</span></span><span class="return-annotation">) -> <span class="n">pandas</span><span class="o">.</span><span class="n">core</span><span class="o">.</span><span class="n">frame</span><span class="o">.</span><span class="n">DataFrame</span>:</span></span>

                <label class="view-source-button" for="optimise_campaign-view-source"><span>View Source</span></label>

    </div>
    <a class="headerlink" href="#optimise_campaign"></a>
            <div class="pdoc-code codehilite"><pre><span></span><span id="optimise_campaign-919"><a href="#optimise_campaign-919"><span class="linenos">919</span></a><span class="k">def</span> <span class="nf">optimise_campaign</span><span class="p">(</span>
</span><span id="optimise_campaign-920"><a href="#optimise_campaign-920"><span class="linenos">920</span></a>    <span class="n">campaign_id</span><span class="p">:</span> <span class="nb">str</span><span class="p">,</span>
</span><span id="optimise_campaign-921"><a href="#optimise_campaign-921"><span class="linenos">921</span></a>    <span class="n">num_points</span><span class="p">:</span> <span class="nb">int</span><span class="p">,</span>
</span><span id="optimise_campaign-922"><a href="#optimise_campaign-922"><span class="linenos">922</span></a>    <span class="n">processor</span><span class="p">:</span> <span class="n">Optional</span><span class="p">[</span><span class="nb">str</span><span class="p">]</span> <span class="o">=</span> <span class="s2">&quot;cpu&quot;</span><span class="p">,</span>
</span><span id="optimise_campaign-923"><a href="#optimise_campaign-923"><span class="linenos">923</span></a>    <span class="n">verbose</span><span class="p">:</span> <span class="n">Optional</span><span class="p">[</span><span class="nb">bool</span><span class="p">]</span> <span class="o">=</span> <span class="kc">False</span><span class="p">,</span>
</span><span id="optimise_campaign-924"><a href="#optimise_campaign-924"><span class="linenos">924</span></a>    <span class="n">debug</span><span class="p">:</span> <span class="n">Optional</span><span class="p">[</span><span class="nb">bool</span><span class="p">]</span> <span class="o">=</span> <span class="kc">False</span><span class="p">,</span>
</span><span id="optimise_campaign-925"><a href="#optimise_campaign-925"><span class="linenos">925</span></a>    <span class="o">**</span><span class="n">kwargs</span><span class="p">,</span>
</span><span id="optimise_campaign-926"><a href="#optimise_campaign-926"><span class="linenos">926</span></a><span class="p">)</span> <span class="o">-&gt;</span> <span class="n">pd</span><span class="o">.</span><span class="n">DataFrame</span><span class="p">:</span>
</span><span id="optimise_campaign-927"><a href="#optimise_campaign-927"><span class="linenos">927</span></a><span class="w">    </span><span class="sd">&quot;&quot;&quot;</span>
</span><span id="optimise_campaign-928"><a href="#optimise_campaign-928"><span class="linenos">928</span></a><span class="sd">    # Optimise campaign</span>
</span><span id="optimise_campaign-929"><a href="#optimise_campaign-929"><span class="linenos">929</span></a>
</span><span id="optimise_campaign-930"><a href="#optimise_campaign-930"><span class="linenos">930</span></a><span class="sd">    Draw new candidate data points by optimizing for &quot;qEI&quot; (Monte Carlo Expected Improvement)</span>
</span><span id="optimise_campaign-931"><a href="#optimise_campaign-931"><span class="linenos">931</span></a><span class="sd">    acquisition function from a pre-trained campaign that exists on the `twinLab` cloud.</span>
</span><span id="optimise_campaign-932"><a href="#optimise_campaign-932"><span class="linenos">932</span></a>
</span><span id="optimise_campaign-933"><a href="#optimise_campaign-933"><span class="linenos">933</span></a><span class="sd">    ## Arguments</span>
</span><span id="optimise_campaign-934"><a href="#optimise_campaign-934"><span class="linenos">934</span></a><span class="sd">    - `campaign_id`: `str`, name of pre-trained campaign to use for predictions</span>
</span><span id="optimise_campaign-935"><a href="#optimise_campaign-935"><span class="linenos">935</span></a><span class="sd">    - `num_points`: `int`, number of samples to draw for each row of the evaluation data</span>
</span><span id="optimise_campaign-936"><a href="#optimise_campaign-936"><span class="linenos">936</span></a><span class="sd">    - `processor`: `str`, Optional, processor to use for sampling (&quot;cpu&quot;; &quot;gpu&quot;)</span>
</span><span id="optimise_campaign-937"><a href="#optimise_campaign-937"><span class="linenos">937</span></a><span class="sd">    - `verbose`: `bool`, Optional, determining level of information returned to the user</span>
</span><span id="optimise_campaign-938"><a href="#optimise_campaign-938"><span class="linenos">938</span></a><span class="sd">    - `debug`: `bool`, Optional, determining level of information logged on the server</span>
</span><span id="optimise_campaign-939"><a href="#optimise_campaign-939"><span class="linenos">939</span></a><span class="sd">    - `acq_kwargs`: `dict`, Optional, specifies the keyword arguments to modify the behavior of</span>
</span><span id="optimise_campaign-940"><a href="#optimise_campaign-940"><span class="linenos">940</span></a><span class="sd">        the acquisition function. This dictionary currently allows only one keyword argument</span>
</span><span id="optimise_campaign-941"><a href="#optimise_campaign-941"><span class="linenos">941</span></a><span class="sd">        - `weights`: `list[float]`, specifies the weightage for different objectives to be</span>
</span><span id="optimise_campaign-942"><a href="#optimise_campaign-942"><span class="linenos">942</span></a><span class="sd">            optimised in a mulit-objective optimisation scenario. By default all weights are equal.</span>
</span><span id="optimise_campaign-943"><a href="#optimise_campaign-943"><span class="linenos">943</span></a><span class="sd">            e.g for a problem with 2 outputs if weights are as follows [1, 0.5], this indicates</span>
</span><span id="optimise_campaign-944"><a href="#optimise_campaign-944"><span class="linenos">944</span></a><span class="sd">            that we focus on maximising the first output dimension twice as much as</span>
</span><span id="optimise_campaign-945"><a href="#optimise_campaign-945"><span class="linenos">945</span></a><span class="sd">            the second output dimension.</span>
</span><span id="optimise_campaign-946"><a href="#optimise_campaign-946"><span class="linenos">946</span></a>
</span><span id="optimise_campaign-947"><a href="#optimise_campaign-947"><span class="linenos">947</span></a><span class="sd">    ## Returns</span>
</span><span id="optimise_campaign-948"><a href="#optimise_campaign-948"><span class="linenos">948</span></a>
</span><span id="optimise_campaign-949"><a href="#optimise_campaign-949"><span class="linenos">949</span></a><span class="sd">    - `Dataframe` containing the recommended sample locations</span>
</span><span id="optimise_campaign-950"><a href="#optimise_campaign-950"><span class="linenos">950</span></a>
</span><span id="optimise_campaign-951"><a href="#optimise_campaign-951"><span class="linenos">951</span></a><span class="sd">    ## Example</span>
</span><span id="optimise_campaign-952"><a href="#optimise_campaign-952"><span class="linenos">952</span></a>
</span><span id="optimise_campaign-953"><a href="#optimise_campaign-953"><span class="linenos">953</span></a><span class="sd">    ```python</span>
</span><span id="optimise_campaign-954"><a href="#optimise_campaign-954"><span class="linenos">954</span></a><span class="sd">    import pandas as pd</span>
</span><span id="optimise_campaign-955"><a href="#optimise_campaign-955"><span class="linenos">955</span></a><span class="sd">    import twinlab as tl</span>
</span><span id="optimise_campaign-956"><a href="#optimise_campaign-956"><span class="linenos">956</span></a>
</span><span id="optimise_campaign-957"><a href="#optimise_campaign-957"><span class="linenos">957</span></a><span class="sd">    df = pd.DataFrame({&#39;X&#39;: [0.0, 0.25, 0.75, 1.0], &#39;y&#39;: [-1.60856306, -0.27526546, -0.34670215, -1.65062947]})</span>
</span><span id="optimise_campaign-958"><a href="#optimise_campaign-958"><span class="linenos">958</span></a><span class="sd">    tl.upload_dataset(df, &quot;my_dataset&quot;)</span>
</span><span id="optimise_campaign-959"><a href="#optimise_campaign-959"><span class="linenos">959</span></a><span class="sd">    params = {</span>
</span><span id="optimise_campaign-960"><a href="#optimise_campaign-960"><span class="linenos">960</span></a><span class="sd">        &quot;dataset_id&quot;: &quot;my_dataset&quot;,</span>
</span><span id="optimise_campaign-961"><a href="#optimise_campaign-961"><span class="linenos">961</span></a><span class="sd">        &quot;inputs&quot;: [&quot;X&quot;],</span>
</span><span id="optimise_campaign-962"><a href="#optimise_campaign-962"><span class="linenos">962</span></a><span class="sd">        &quot;outputs&quot;: [&quot;y&quot;],</span>
</span><span id="optimise_campaign-963"><a href="#optimise_campaign-963"><span class="linenos">963</span></a><span class="sd">    }</span>
</span><span id="optimise_campaign-964"><a href="#optimise_campaign-964"><span class="linenos">964</span></a><span class="sd">    tl.train_campaign(params, &quot;my_campaign&quot;)</span>
</span><span id="optimise_campaign-965"><a href="#optimise_campaign-965"><span class="linenos">965</span></a><span class="sd">    n = 1</span>
</span><span id="optimise_campaign-966"><a href="#optimise_campaign-966"><span class="linenos">966</span></a><span class="sd">    df = tl.optimise_campaign(&quot;my_campaign&quot;, n)</span>
</span><span id="optimise_campaign-967"><a href="#optimise_campaign-967"><span class="linenos">967</span></a><span class="sd">    print(df)</span>
</span><span id="optimise_campaign-968"><a href="#optimise_campaign-968"><span class="linenos">968</span></a><span class="sd">    ```</span>
</span><span id="optimise_campaign-969"><a href="#optimise_campaign-969"><span class="linenos">969</span></a><span class="sd">    &quot;&quot;&quot;</span>
</span><span id="optimise_campaign-970"><a href="#optimise_campaign-970"><span class="linenos">970</span></a>
</span><span id="optimise_campaign-971"><a href="#optimise_campaign-971"><span class="linenos">971</span></a>    <span class="n">csv</span> <span class="o">=</span> <span class="n">_use_campaign</span><span class="p">(</span>
</span><span id="optimise_campaign-972"><a href="#optimise_campaign-972"><span class="linenos">972</span></a>        <span class="n">campaign_id</span><span class="p">,</span>
</span><span id="optimise_campaign-973"><a href="#optimise_campaign-973"><span class="linenos">973</span></a>        <span class="n">method</span><span class="o">=</span><span class="s2">&quot;get_candidate_points&quot;</span><span class="p">,</span>
</span><span id="optimise_campaign-974"><a href="#optimise_campaign-974"><span class="linenos">974</span></a>        <span class="n">acq_func</span><span class="o">=</span><span class="s2">&quot;qEI&quot;</span><span class="p">,</span>
</span><span id="optimise_campaign-975"><a href="#optimise_campaign-975"><span class="linenos">975</span></a>        <span class="n">num_points</span><span class="o">=</span><span class="n">num_points</span><span class="p">,</span>
</span><span id="optimise_campaign-976"><a href="#optimise_campaign-976"><span class="linenos">976</span></a>        <span class="n">processor</span><span class="o">=</span><span class="n">processor</span><span class="p">,</span>
</span><span id="optimise_campaign-977"><a href="#optimise_campaign-977"><span class="linenos">977</span></a>        <span class="n">verbose</span><span class="o">=</span><span class="n">verbose</span><span class="p">,</span>
</span><span id="optimise_campaign-978"><a href="#optimise_campaign-978"><span class="linenos">978</span></a>        <span class="n">debug</span><span class="o">=</span><span class="n">debug</span><span class="p">,</span>
</span><span id="optimise_campaign-979"><a href="#optimise_campaign-979"><span class="linenos">979</span></a>        <span class="o">**</span><span class="n">kwargs</span><span class="p">,</span>
</span><span id="optimise_campaign-980"><a href="#optimise_campaign-980"><span class="linenos">980</span></a>    <span class="p">)</span>
</span><span id="optimise_campaign-981"><a href="#optimise_campaign-981"><span class="linenos">981</span></a>    <span class="n">df</span> <span class="o">=</span> <span class="n">pd</span><span class="o">.</span><span class="n">read_csv</span><span class="p">(</span><span class="n">csv</span><span class="p">,</span> <span class="n">sep</span><span class="o">=</span><span class="s2">&quot;,&quot;</span><span class="p">)</span>
</span><span id="optimise_campaign-982"><a href="#optimise_campaign-982"><span class="linenos">982</span></a>    <span class="k">if</span> <span class="n">verbose</span><span class="p">:</span>
</span><span id="optimise_campaign-983"><a href="#optimise_campaign-983"><span class="linenos">983</span></a>        <span class="nb">print</span><span class="p">(</span><span class="s2">&quot;Candidate points:&quot;</span><span class="p">)</span>
</span><span id="optimise_campaign-984"><a href="#optimise_campaign-984"><span class="linenos">984</span></a>        <span class="nb">print</span><span class="p">(</span><span class="n">df</span><span class="p">)</span>
</span><span id="optimise_campaign-985"><a href="#optimise_campaign-985"><span class="linenos">985</span></a>    <span class="k">return</span> <span class="n">df</span>
</span></pre></div>


            <div class="docstring"><h1 id="optimise-campaign">Optimise campaign</h1>

<p>Draw new candidate data points by optimizing for "qEI" (Monte Carlo Expected Improvement)
acquisition function from a pre-trained campaign that exists on the <code>twinLab</code> cloud.</p>

<h2 id="arguments">Arguments</h2>

<ul>
<li><code>campaign_id</code>: <code>str</code>, name of pre-trained campaign to use for predictions</li>
<li><code>num_points</code>: <code>int</code>, number of samples to draw for each row of the evaluation data</li>
<li><code>processor</code>: <code>str</code>, Optional, processor to use for sampling ("cpu"; "gpu")</li>
<li><code>verbose</code>: <code>bool</code>, Optional, determining level of information returned to the user</li>
<li><code>debug</code>: <code>bool</code>, Optional, determining level of information logged on the server</li>
<li><code>acq_kwargs</code>: <code>dict</code>, Optional, specifies the keyword arguments to modify the behavior of
the acquisition function. This dictionary currently allows only one keyword argument
<ul>
<li><code>weights</code>: <code>list[float]</code>, specifies the weightage for different objectives to be
optimised in a mulit-objective optimisation scenario. By default all weights are equal.
e.g for a problem with 2 outputs if weights are as follows [1, 0.5], this indicates
that we focus on maximising the first output dimension twice as much as
the second output dimension.</li>
</ul></li>
</ul>

<h2 id="returns">Returns</h2>

<ul>
<li><code>Dataframe</code> containing the recommended sample locations</li>
</ul>

<h2 id="example">Example</h2>

<div class="pdoc-code codehilite">
<pre><span></span><code><span class="kn">import</span> <span class="nn">pandas</span> <span class="k">as</span> <span class="nn">pd</span>
<span class="kn">import</span> <span class="nn">twinlab</span> <span class="k">as</span> <span class="nn">tl</span>

<span class="n">df</span> <span class="o">=</span> <span class="n">pd</span><span class="o">.</span><span class="n">DataFrame</span><span class="p">({</span><span class="s1">&#39;X&#39;</span><span class="p">:</span> <span class="p">[</span><span class="mf">0.0</span><span class="p">,</span> <span class="mf">0.25</span><span class="p">,</span> <span class="mf">0.75</span><span class="p">,</span> <span class="mf">1.0</span><span class="p">],</span> <span class="s1">&#39;y&#39;</span><span class="p">:</span> <span class="p">[</span><span class="o">-</span><span class="mf">1.60856306</span><span class="p">,</span> <span class="o">-</span><span class="mf">0.27526546</span><span class="p">,</span> <span class="o">-</span><span class="mf">0.34670215</span><span class="p">,</span> <span class="o">-</span><span class="mf">1.65062947</span><span class="p">]})</span>
<span class="n">tl</span><span class="o">.</span><span class="n">upload_dataset</span><span class="p">(</span><span class="n">df</span><span class="p">,</span> <span class="s2">&quot;my_dataset&quot;</span><span class="p">)</span>
<span class="n">params</span> <span class="o">=</span> <span class="p">{</span>
    <span class="s2">&quot;dataset_id&quot;</span><span class="p">:</span> <span class="s2">&quot;my_dataset&quot;</span><span class="p">,</span>
    <span class="s2">&quot;inputs&quot;</span><span class="p">:</span> <span class="p">[</span><span class="s2">&quot;X&quot;</span><span class="p">],</span>
    <span class="s2">&quot;outputs&quot;</span><span class="p">:</span> <span class="p">[</span><span class="s2">&quot;y&quot;</span><span class="p">],</span>
<span class="p">}</span>
<span class="n">tl</span><span class="o">.</span><span class="n">train_campaign</span><span class="p">(</span><span class="n">params</span><span class="p">,</span> <span class="s2">&quot;my_campaign&quot;</span><span class="p">)</span>
<span class="n">n</span> <span class="o">=</span> <span class="mi">1</span>
<span class="n">df</span> <span class="o">=</span> <span class="n">tl</span><span class="o">.</span><span class="n">optimise_campaign</span><span class="p">(</span><span class="s2">&quot;my_campaign&quot;</span><span class="p">,</span> <span class="n">n</span><span class="p">)</span>
<span class="nb">print</span><span class="p">(</span><span class="n">df</span><span class="p">)</span>
</code></pre>
</div>
</div>


                </section>
                <section id="solve_inverse_campaign">
                            <input id="solve_inverse_campaign-view-source" class="view-source-toggle-state" type="checkbox" aria-hidden="true" tabindex="-1">
<div class="attr function">
            
        <span class="def">def</span>
        <span class="name">solve_inverse_campaign</span><span class="signature pdoc-code multiline">(<span class="param">	<span class="n">campaign_id</span><span class="p">:</span> <span class="nb">str</span>,</span><span class="param">	<span class="n">filepath_or_df</span><span class="p">:</span> <span class="n">Union</span><span class="p">[</span><span class="nb">str</span><span class="p">,</span> <span class="n">pandas</span><span class="o">.</span><span class="n">core</span><span class="o">.</span><span class="n">frame</span><span class="o">.</span><span class="n">DataFrame</span><span class="p">]</span>,</span><span class="param">	<span class="n">filepath_or_df_std</span><span class="p">:</span> <span class="n">Union</span><span class="p">[</span><span class="nb">str</span><span class="p">,</span> <span class="n">pandas</span><span class="o">.</span><span class="n">core</span><span class="o">.</span><span class="n">frame</span><span class="o">.</span><span class="n">DataFrame</span><span class="p">]</span>,</span><span class="param">	<span class="n">processor</span><span class="p">:</span> <span class="n">Optional</span><span class="p">[</span><span class="nb">str</span><span class="p">]</span> <span class="o">=</span> <span class="s1">&#39;cpu&#39;</span>,</span><span class="param">	<span class="n">verbose</span><span class="p">:</span> <span class="n">Optional</span><span class="p">[</span><span class="nb">bool</span><span class="p">]</span> <span class="o">=</span> <span class="kc">False</span>,</span><span class="param">	<span class="n">debug</span><span class="p">:</span> <span class="n">Optional</span><span class="p">[</span><span class="nb">bool</span><span class="p">]</span> <span class="o">=</span> <span class="kc">False</span>,</span><span class="param">	<span class="o">**</span><span class="n">kwargs</span></span><span class="return-annotation">) -> <span class="n">pandas</span><span class="o">.</span><span class="n">core</span><span class="o">.</span><span class="n">frame</span><span class="o">.</span><span class="n">DataFrame</span>:</span></span>

                <label class="view-source-button" for="solve_inverse_campaign-view-source"><span>View Source</span></label>

    </div>
    <a class="headerlink" href="#solve_inverse_campaign"></a>
            <div class="pdoc-code codehilite"><pre><span></span><span id="solve_inverse_campaign-989"><a href="#solve_inverse_campaign-989"><span class="linenos"> 989</span></a><span class="k">def</span> <span class="nf">solve_inverse_campaign</span><span class="p">(</span>
</span><span id="solve_inverse_campaign-990"><a href="#solve_inverse_campaign-990"><span class="linenos"> 990</span></a>    <span class="n">campaign_id</span><span class="p">:</span> <span class="nb">str</span><span class="p">,</span>
</span><span id="solve_inverse_campaign-991"><a href="#solve_inverse_campaign-991"><span class="linenos"> 991</span></a>    <span class="n">filepath_or_df</span><span class="p">:</span> <span class="n">Union</span><span class="p">[</span><span class="nb">str</span><span class="p">,</span> <span class="n">pd</span><span class="o">.</span><span class="n">DataFrame</span><span class="p">],</span>
</span><span id="solve_inverse_campaign-992"><a href="#solve_inverse_campaign-992"><span class="linenos"> 992</span></a>    <span class="n">filepath_or_df_std</span><span class="p">:</span> <span class="n">Union</span><span class="p">[</span><span class="nb">str</span><span class="p">,</span> <span class="n">pd</span><span class="o">.</span><span class="n">DataFrame</span><span class="p">],</span>
</span><span id="solve_inverse_campaign-993"><a href="#solve_inverse_campaign-993"><span class="linenos"> 993</span></a>    <span class="n">processor</span><span class="p">:</span> <span class="n">Optional</span><span class="p">[</span><span class="nb">str</span><span class="p">]</span> <span class="o">=</span> <span class="s2">&quot;cpu&quot;</span><span class="p">,</span>
</span><span id="solve_inverse_campaign-994"><a href="#solve_inverse_campaign-994"><span class="linenos"> 994</span></a>    <span class="n">verbose</span><span class="p">:</span> <span class="n">Optional</span><span class="p">[</span><span class="nb">bool</span><span class="p">]</span> <span class="o">=</span> <span class="kc">False</span><span class="p">,</span>
</span><span id="solve_inverse_campaign-995"><a href="#solve_inverse_campaign-995"><span class="linenos"> 995</span></a>    <span class="n">debug</span><span class="p">:</span> <span class="n">Optional</span><span class="p">[</span><span class="nb">bool</span><span class="p">]</span> <span class="o">=</span> <span class="kc">False</span><span class="p">,</span>
</span><span id="solve_inverse_campaign-996"><a href="#solve_inverse_campaign-996"><span class="linenos"> 996</span></a>    <span class="o">**</span><span class="n">kwargs</span><span class="p">,</span>
</span><span id="solve_inverse_campaign-997"><a href="#solve_inverse_campaign-997"><span class="linenos"> 997</span></a><span class="p">)</span> <span class="o">-&gt;</span> <span class="n">pd</span><span class="o">.</span><span class="n">DataFrame</span><span class="p">:</span>
</span><span id="solve_inverse_campaign-998"><a href="#solve_inverse_campaign-998"><span class="linenos"> 998</span></a><span class="w">    </span><span class="sd">&quot;&quot;&quot;</span>
</span><span id="solve_inverse_campaign-999"><a href="#solve_inverse_campaign-999"><span class="linenos"> 999</span></a><span class="sd">    # Inverse modelling on campaign</span>
</span><span id="solve_inverse_campaign-1000"><a href="#solve_inverse_campaign-1000"><span class="linenos">1000</span></a>
</span><span id="solve_inverse_campaign-1001"><a href="#solve_inverse_campaign-1001"><span class="linenos">1001</span></a><span class="sd">    Given a set of observations, inverse modelling finds the model that would best suit the data.</span>
</span><span id="solve_inverse_campaign-1002"><a href="#solve_inverse_campaign-1002"><span class="linenos">1002</span></a>
</span><span id="solve_inverse_campaign-1003"><a href="#solve_inverse_campaign-1003"><span class="linenos">1003</span></a><span class="sd">    ## Arguments</span>
</span><span id="solve_inverse_campaign-1004"><a href="#solve_inverse_campaign-1004"><span class="linenos">1004</span></a><span class="sd">    - `campaign_id`: `str`; name of pre-trained campaign to use for predictions</span>
</span><span id="solve_inverse_campaign-1005"><a href="#solve_inverse_campaign-1005"><span class="linenos">1005</span></a><span class="sd">    - `data_csv`: `DataFrame`; a DataFrame of observations</span>
</span><span id="solve_inverse_campaign-1006"><a href="#solve_inverse_campaign-1006"><span class="linenos">1006</span></a><span class="sd">    - `data_std_csv` : `DataFrame`; a DataFrame of errors on the observations</span>
</span><span id="solve_inverse_campaign-1007"><a href="#solve_inverse_campaign-1007"><span class="linenos">1007</span></a><span class="sd">    - `processor`: `str`; processor to use for sampling (&quot;cpu&quot;; &quot;gpu&quot;)</span>
</span><span id="solve_inverse_campaign-1008"><a href="#solve_inverse_campaign-1008"><span class="linenos">1008</span></a><span class="sd">    - `verbose`: `bool` determining level of information returned to the user</span>
</span><span id="solve_inverse_campaign-1009"><a href="#solve_inverse_campaign-1009"><span class="linenos">1009</span></a><span class="sd">    - `debug`: `bool` determining level of information logged on the server</span>
</span><span id="solve_inverse_campaign-1010"><a href="#solve_inverse_campaign-1010"><span class="linenos">1010</span></a>
</span><span id="solve_inverse_campaign-1011"><a href="#solve_inverse_campaign-1011"><span class="linenos">1011</span></a><span class="sd">    ## Returns</span>
</span><span id="solve_inverse_campaign-1012"><a href="#solve_inverse_campaign-1012"><span class="linenos">1012</span></a>
</span><span id="solve_inverse_campaign-1013"><a href="#solve_inverse_campaign-1013"><span class="linenos">1013</span></a><span class="sd">    - `Dataframe` containing the recommended model statistics</span>
</span><span id="solve_inverse_campaign-1014"><a href="#solve_inverse_campaign-1014"><span class="linenos">1014</span></a>
</span><span id="solve_inverse_campaign-1015"><a href="#solve_inverse_campaign-1015"><span class="linenos">1015</span></a><span class="sd">    ## Example</span>
</span><span id="solve_inverse_campaign-1016"><a href="#solve_inverse_campaign-1016"><span class="linenos">1016</span></a>
</span><span id="solve_inverse_campaign-1017"><a href="#solve_inverse_campaign-1017"><span class="linenos">1017</span></a><span class="sd">    ```python</span>
</span><span id="solve_inverse_campaign-1018"><a href="#solve_inverse_campaign-1018"><span class="linenos">1018</span></a><span class="sd">    import pandas as pd</span>
</span><span id="solve_inverse_campaign-1019"><a href="#solve_inverse_campaign-1019"><span class="linenos">1019</span></a><span class="sd">    import twinlab as tl</span>
</span><span id="solve_inverse_campaign-1020"><a href="#solve_inverse_campaign-1020"><span class="linenos">1020</span></a>
</span><span id="solve_inverse_campaign-1021"><a href="#solve_inverse_campaign-1021"><span class="linenos">1021</span></a><span class="sd">    df = pd.DataFrame({&#39;X&#39;: [1, 2, 3, 4], &#39;y&#39;: [1, 4, 9, 16]})</span>
</span><span id="solve_inverse_campaign-1022"><a href="#solve_inverse_campaign-1022"><span class="linenos">1022</span></a><span class="sd">    tl.upload_dataset(df, &quot;my_dataset&quot;)</span>
</span><span id="solve_inverse_campaign-1023"><a href="#solve_inverse_campaign-1023"><span class="linenos">1023</span></a><span class="sd">    params = {</span>
</span><span id="solve_inverse_campaign-1024"><a href="#solve_inverse_campaign-1024"><span class="linenos">1024</span></a><span class="sd">        &quot;dataset_id&quot;: &quot;my_dataset&quot;,</span>
</span><span id="solve_inverse_campaign-1025"><a href="#solve_inverse_campaign-1025"><span class="linenos">1025</span></a><span class="sd">        &quot;inputs&quot;: [&quot;X&quot;],</span>
</span><span id="solve_inverse_campaign-1026"><a href="#solve_inverse_campaign-1026"><span class="linenos">1026</span></a><span class="sd">        &quot;outputs&quot;: [&quot;y&quot;],</span>
</span><span id="solve_inverse_campaign-1027"><a href="#solve_inverse_campaign-1027"><span class="linenos">1027</span></a><span class="sd">    }</span>
</span><span id="solve_inverse_campaign-1028"><a href="#solve_inverse_campaign-1028"><span class="linenos">1028</span></a><span class="sd">    tl.train_campaign(params, &quot;my_campaign&quot;)</span>
</span><span id="solve_inverse_campaign-1029"><a href="#solve_inverse_campaign-1029"><span class="linenos">1029</span></a><span class="sd">    data_csv = pd.DataFrame({&#39;y&#39;: [1]})</span>
</span><span id="solve_inverse_campaign-1030"><a href="#solve_inverse_campaign-1030"><span class="linenos">1030</span></a><span class="sd">    data_std_csv = pd.DataFrame({&#39;y&#39;: [0.498]})</span>
</span><span id="solve_inverse_campaign-1031"><a href="#solve_inverse_campaign-1031"><span class="linenos">1031</span></a><span class="sd">    df = tl.solve_inverse_campaign(&quot;my_campaign&quot;, data_csv, data_std_csv)</span>
</span><span id="solve_inverse_campaign-1032"><a href="#solve_inverse_campaign-1032"><span class="linenos">1032</span></a><span class="sd">    print(df)</span>
</span><span id="solve_inverse_campaign-1033"><a href="#solve_inverse_campaign-1033"><span class="linenos">1033</span></a><span class="sd">    ```</span>
</span><span id="solve_inverse_campaign-1034"><a href="#solve_inverse_campaign-1034"><span class="linenos">1034</span></a><span class="sd">    &quot;&quot;&quot;</span>
</span><span id="solve_inverse_campaign-1035"><a href="#solve_inverse_campaign-1035"><span class="linenos">1035</span></a>    <span class="n">csv</span> <span class="o">=</span> <span class="n">_use_campaign</span><span class="p">(</span>
</span><span id="solve_inverse_campaign-1036"><a href="#solve_inverse_campaign-1036"><span class="linenos">1036</span></a>        <span class="n">campaign_id</span><span class="p">,</span>
</span><span id="solve_inverse_campaign-1037"><a href="#solve_inverse_campaign-1037"><span class="linenos">1037</span></a>        <span class="n">method</span><span class="o">=</span><span class="s2">&quot;solve_inverse&quot;</span><span class="p">,</span>
</span><span id="solve_inverse_campaign-1038"><a href="#solve_inverse_campaign-1038"><span class="linenos">1038</span></a>        <span class="n">filepath_or_df</span><span class="o">=</span><span class="n">filepath_or_df</span><span class="p">,</span>
</span><span id="solve_inverse_campaign-1039"><a href="#solve_inverse_campaign-1039"><span class="linenos">1039</span></a>        <span class="n">filepath_or_df_std</span><span class="o">=</span><span class="n">filepath_or_df_std</span><span class="p">,</span>
</span><span id="solve_inverse_campaign-1040"><a href="#solve_inverse_campaign-1040"><span class="linenos">1040</span></a>        <span class="n">processor</span><span class="o">=</span><span class="n">processor</span><span class="p">,</span>
</span><span id="solve_inverse_campaign-1041"><a href="#solve_inverse_campaign-1041"><span class="linenos">1041</span></a>        <span class="n">verbose</span><span class="o">=</span><span class="n">verbose</span><span class="p">,</span>
</span><span id="solve_inverse_campaign-1042"><a href="#solve_inverse_campaign-1042"><span class="linenos">1042</span></a>        <span class="n">debug</span><span class="o">=</span><span class="n">debug</span><span class="p">,</span>
</span><span id="solve_inverse_campaign-1043"><a href="#solve_inverse_campaign-1043"><span class="linenos">1043</span></a>        <span class="o">**</span><span class="n">kwargs</span><span class="p">,</span>
</span><span id="solve_inverse_campaign-1044"><a href="#solve_inverse_campaign-1044"><span class="linenos">1044</span></a>    <span class="p">)</span>
</span><span id="solve_inverse_campaign-1045"><a href="#solve_inverse_campaign-1045"><span class="linenos">1045</span></a>
</span><span id="solve_inverse_campaign-1046"><a href="#solve_inverse_campaign-1046"><span class="linenos">1046</span></a>    <span class="n">df</span> <span class="o">=</span> <span class="n">pd</span><span class="o">.</span><span class="n">read_csv</span><span class="p">(</span><span class="n">csv</span><span class="p">,</span> <span class="n">sep</span><span class="o">=</span><span class="s2">&quot;,&quot;</span><span class="p">)</span>
</span><span id="solve_inverse_campaign-1047"><a href="#solve_inverse_campaign-1047"><span class="linenos">1047</span></a>    <span class="k">if</span> <span class="n">verbose</span><span class="p">:</span>
</span><span id="solve_inverse_campaign-1048"><a href="#solve_inverse_campaign-1048"><span class="linenos">1048</span></a>        <span class="nb">print</span><span class="p">(</span><span class="s2">&quot;Inverse model statistics:&quot;</span><span class="p">)</span>
</span><span id="solve_inverse_campaign-1049"><a href="#solve_inverse_campaign-1049"><span class="linenos">1049</span></a>        <span class="nb">print</span><span class="p">(</span><span class="n">df</span><span class="p">)</span>
</span><span id="solve_inverse_campaign-1050"><a href="#solve_inverse_campaign-1050"><span class="linenos">1050</span></a>    <span class="k">return</span> <span class="n">df</span>
</span></pre></div>


            <div class="docstring"><h1 id="inverse-modelling-on-campaign">Inverse modelling on campaign</h1>

<p>Given a set of observations, inverse modelling finds the model that would best suit the data.</p>

<h2 id="arguments">Arguments</h2>

<ul>
<li><code>campaign_id</code>: <code>str</code>; name of pre-trained campaign to use for predictions</li>
<li><code>data_csv</code>: <code>DataFrame</code>; a DataFrame of observations</li>
<li><code>data_std_csv</code> : <code>DataFrame</code>; a DataFrame of errors on the observations</li>
<li><code>processor</code>: <code>str</code>; processor to use for sampling ("cpu"; "gpu")</li>
<li><code>verbose</code>: <code>bool</code> determining level of information returned to the user</li>
<li><code>debug</code>: <code>bool</code> determining level of information logged on the server</li>
</ul>

<h2 id="returns">Returns</h2>

<ul>
<li><code>Dataframe</code> containing the recommended model statistics</li>
</ul>

<h2 id="example">Example</h2>

<div class="pdoc-code codehilite">
<pre><span></span><code><span class="kn">import</span> <span class="nn">pandas</span> <span class="k">as</span> <span class="nn">pd</span>
<span class="kn">import</span> <span class="nn">twinlab</span> <span class="k">as</span> <span class="nn">tl</span>

<span class="n">df</span> <span class="o">=</span> <span class="n">pd</span><span class="o">.</span><span class="n">DataFrame</span><span class="p">({</span><span class="s1">&#39;X&#39;</span><span class="p">:</span> <span class="p">[</span><span class="mi">1</span><span class="p">,</span> <span class="mi">2</span><span class="p">,</span> <span class="mi">3</span><span class="p">,</span> <span class="mi">4</span><span class="p">],</span> <span class="s1">&#39;y&#39;</span><span class="p">:</span> <span class="p">[</span><span class="mi">1</span><span class="p">,</span> <span class="mi">4</span><span class="p">,</span> <span class="mi">9</span><span class="p">,</span> <span class="mi">16</span><span class="p">]})</span>
<span class="n">tl</span><span class="o">.</span><span class="n">upload_dataset</span><span class="p">(</span><span class="n">df</span><span class="p">,</span> <span class="s2">&quot;my_dataset&quot;</span><span class="p">)</span>
<span class="n">params</span> <span class="o">=</span> <span class="p">{</span>
    <span class="s2">&quot;dataset_id&quot;</span><span class="p">:</span> <span class="s2">&quot;my_dataset&quot;</span><span class="p">,</span>
    <span class="s2">&quot;inputs&quot;</span><span class="p">:</span> <span class="p">[</span><span class="s2">&quot;X&quot;</span><span class="p">],</span>
    <span class="s2">&quot;outputs&quot;</span><span class="p">:</span> <span class="p">[</span><span class="s2">&quot;y&quot;</span><span class="p">],</span>
<span class="p">}</span>
<span class="n">tl</span><span class="o">.</span><span class="n">train_campaign</span><span class="p">(</span><span class="n">params</span><span class="p">,</span> <span class="s2">&quot;my_campaign&quot;</span><span class="p">)</span>
<span class="n">data_csv</span> <span class="o">=</span> <span class="n">pd</span><span class="o">.</span><span class="n">DataFrame</span><span class="p">({</span><span class="s1">&#39;y&#39;</span><span class="p">:</span> <span class="p">[</span><span class="mi">1</span><span class="p">]})</span>
<span class="n">data_std_csv</span> <span class="o">=</span> <span class="n">pd</span><span class="o">.</span><span class="n">DataFrame</span><span class="p">({</span><span class="s1">&#39;y&#39;</span><span class="p">:</span> <span class="p">[</span><span class="mf">0.498</span><span class="p">]})</span>
<span class="n">df</span> <span class="o">=</span> <span class="n">tl</span><span class="o">.</span><span class="n">solve_inverse_campaign</span><span class="p">(</span><span class="s2">&quot;my_campaign&quot;</span><span class="p">,</span> <span class="n">data_csv</span><span class="p">,</span> <span class="n">data_std_csv</span><span class="p">)</span>
<span class="nb">print</span><span class="p">(</span><span class="n">df</span><span class="p">)</span>
</code></pre>
</div>
</div>


                </section>
                <section id="delete_campaign">
                            <input id="delete_campaign-view-source" class="view-source-toggle-state" type="checkbox" aria-hidden="true" tabindex="-1">
<div class="attr function">
            
        <span class="def">def</span>
        <span class="name">delete_campaign</span><span class="signature pdoc-code multiline">(<span class="param">	<span class="n">campaign_id</span><span class="p">:</span> <span class="nb">str</span>,</span><span class="param">	<span class="n">verbose</span><span class="p">:</span> <span class="n">Optional</span><span class="p">[</span><span class="nb">bool</span><span class="p">]</span> <span class="o">=</span> <span class="kc">False</span>,</span><span class="param">	<span class="n">debug</span><span class="p">:</span> <span class="n">Optional</span><span class="p">[</span><span class="nb">bool</span><span class="p">]</span> <span class="o">=</span> <span class="kc">False</span></span><span class="return-annotation">) -> <span class="kc">None</span>:</span></span>

                <label class="view-source-button" for="delete_campaign-view-source"><span>View Source</span></label>

    </div>
    <a class="headerlink" href="#delete_campaign"></a>
            <div class="pdoc-code codehilite"><pre><span></span><span id="delete_campaign-1054"><a href="#delete_campaign-1054"><span class="linenos">1054</span></a><span class="k">def</span> <span class="nf">delete_campaign</span><span class="p">(</span>
</span><span id="delete_campaign-1055"><a href="#delete_campaign-1055"><span class="linenos">1055</span></a>    <span class="n">campaign_id</span><span class="p">:</span> <span class="nb">str</span><span class="p">,</span> <span class="n">verbose</span><span class="p">:</span> <span class="n">Optional</span><span class="p">[</span><span class="nb">bool</span><span class="p">]</span> <span class="o">=</span> <span class="kc">False</span><span class="p">,</span> <span class="n">debug</span><span class="p">:</span> <span class="n">Optional</span><span class="p">[</span><span class="nb">bool</span><span class="p">]</span> <span class="o">=</span> <span class="kc">False</span>
</span><span id="delete_campaign-1056"><a href="#delete_campaign-1056"><span class="linenos">1056</span></a><span class="p">)</span> <span class="o">-&gt;</span> <span class="kc">None</span><span class="p">:</span>
</span><span id="delete_campaign-1057"><a href="#delete_campaign-1057"><span class="linenos">1057</span></a><span class="w">    </span><span class="sd">&quot;&quot;&quot;</span>
</span><span id="delete_campaign-1058"><a href="#delete_campaign-1058"><span class="linenos">1058</span></a><span class="sd">    # Delete campaign</span>
</span><span id="delete_campaign-1059"><a href="#delete_campaign-1059"><span class="linenos">1059</span></a>
</span><span id="delete_campaign-1060"><a href="#delete_campaign-1060"><span class="linenos">1060</span></a><span class="sd">    Delete campaign from the `twinLab` cloud.</span>
</span><span id="delete_campaign-1061"><a href="#delete_campaign-1061"><span class="linenos">1061</span></a>
</span><span id="delete_campaign-1062"><a href="#delete_campaign-1062"><span class="linenos">1062</span></a><span class="sd">    ## Arguments</span>
</span><span id="delete_campaign-1063"><a href="#delete_campaign-1063"><span class="linenos">1063</span></a>
</span><span id="delete_campaign-1064"><a href="#delete_campaign-1064"><span class="linenos">1064</span></a><span class="sd">    - `campaign_id`: `str`; name of trained campaign to delete from the cloud</span>
</span><span id="delete_campaign-1065"><a href="#delete_campaign-1065"><span class="linenos">1065</span></a><span class="sd">    - `verbose`: `bool`, Optional, determining level of information returned to the user</span>
</span><span id="delete_campaign-1066"><a href="#delete_campaign-1066"><span class="linenos">1066</span></a><span class="sd">    - `debug`: `bool`, Optional, determining level of information logged on the server</span>
</span><span id="delete_campaign-1067"><a href="#delete_campaign-1067"><span class="linenos">1067</span></a>
</span><span id="delete_campaign-1068"><a href="#delete_campaign-1068"><span class="linenos">1068</span></a><span class="sd">    ## Example</span>
</span><span id="delete_campaign-1069"><a href="#delete_campaign-1069"><span class="linenos">1069</span></a>
</span><span id="delete_campaign-1070"><a href="#delete_campaign-1070"><span class="linenos">1070</span></a><span class="sd">    ```python</span>
</span><span id="delete_campaign-1071"><a href="#delete_campaign-1071"><span class="linenos">1071</span></a><span class="sd">    import pandas as pd</span>
</span><span id="delete_campaign-1072"><a href="#delete_campaign-1072"><span class="linenos">1072</span></a><span class="sd">    import twinlab as tl</span>
</span><span id="delete_campaign-1073"><a href="#delete_campaign-1073"><span class="linenos">1073</span></a>
</span><span id="delete_campaign-1074"><a href="#delete_campaign-1074"><span class="linenos">1074</span></a><span class="sd">    df = pd.DataFrame({&#39;X&#39;: [1, 2, 3, 4], &#39;y&#39;: [1, 4, 9, 16]})</span>
</span><span id="delete_campaign-1075"><a href="#delete_campaign-1075"><span class="linenos">1075</span></a><span class="sd">    tl.upload_dataset(df, &quot;my_dataset&quot;)</span>
</span><span id="delete_campaign-1076"><a href="#delete_campaign-1076"><span class="linenos">1076</span></a><span class="sd">    params = {</span>
</span><span id="delete_campaign-1077"><a href="#delete_campaign-1077"><span class="linenos">1077</span></a><span class="sd">        &quot;dataset_id&quot;: &quot;my_dataset&quot;,</span>
</span><span id="delete_campaign-1078"><a href="#delete_campaign-1078"><span class="linenos">1078</span></a><span class="sd">        &quot;inputs&quot;: [&quot;X&quot;],</span>
</span><span id="delete_campaign-1079"><a href="#delete_campaign-1079"><span class="linenos">1079</span></a><span class="sd">        &quot;outputs&quot;: [&quot;y&quot;],</span>
</span><span id="delete_campaign-1080"><a href="#delete_campaign-1080"><span class="linenos">1080</span></a><span class="sd">    }</span>
</span><span id="delete_campaign-1081"><a href="#delete_campaign-1081"><span class="linenos">1081</span></a><span class="sd">    tl.train_campaign(params, &quot;my_campaign&quot;)</span>
</span><span id="delete_campaign-1082"><a href="#delete_campaign-1082"><span class="linenos">1082</span></a><span class="sd">    tl.delete_campaign(&quot;my_campaign&quot;)</span>
</span><span id="delete_campaign-1083"><a href="#delete_campaign-1083"><span class="linenos">1083</span></a><span class="sd">    ```</span>
</span><span id="delete_campaign-1084"><a href="#delete_campaign-1084"><span class="linenos">1084</span></a><span class="sd">    &quot;&quot;&quot;</span>
</span><span id="delete_campaign-1085"><a href="#delete_campaign-1085"><span class="linenos">1085</span></a>    <span class="n">response</span> <span class="o">=</span> <span class="n">api</span><span class="o">.</span><span class="n">delete_model</span><span class="p">(</span><span class="n">campaign_id</span><span class="p">,</span> <span class="n">verbose</span><span class="o">=</span><span class="n">debug</span><span class="p">)</span>
</span><span id="delete_campaign-1086"><a href="#delete_campaign-1086"><span class="linenos">1086</span></a>    <span class="k">if</span> <span class="n">verbose</span><span class="p">:</span>
</span><span id="delete_campaign-1087"><a href="#delete_campaign-1087"><span class="linenos">1087</span></a>        <span class="n">message</span> <span class="o">=</span> <span class="n">_get_message</span><span class="p">(</span><span class="n">response</span><span class="p">)</span>
</span><span id="delete_campaign-1088"><a href="#delete_campaign-1088"><span class="linenos">1088</span></a>        <span class="nb">print</span><span class="p">(</span><span class="n">message</span><span class="p">)</span>
</span></pre></div>


            <div class="docstring"><h1 id="delete-campaign">Delete campaign</h1>

<p>Delete campaign from the <code>twinLab</code> cloud.</p>

<h2 id="arguments">Arguments</h2>

<ul>
<li><code>campaign_id</code>: <code>str</code>; name of trained campaign to delete from the cloud</li>
<li><code>verbose</code>: <code>bool</code>, Optional, determining level of information returned to the user</li>
<li><code>debug</code>: <code>bool</code>, Optional, determining level of information logged on the server</li>
</ul>

<h2 id="example">Example</h2>

<div class="pdoc-code codehilite">
<pre><span></span><code><span class="kn">import</span> <span class="nn">pandas</span> <span class="k">as</span> <span class="nn">pd</span>
<span class="kn">import</span> <span class="nn">twinlab</span> <span class="k">as</span> <span class="nn">tl</span>

<span class="n">df</span> <span class="o">=</span> <span class="n">pd</span><span class="o">.</span><span class="n">DataFrame</span><span class="p">({</span><span class="s1">&#39;X&#39;</span><span class="p">:</span> <span class="p">[</span><span class="mi">1</span><span class="p">,</span> <span class="mi">2</span><span class="p">,</span> <span class="mi">3</span><span class="p">,</span> <span class="mi">4</span><span class="p">],</span> <span class="s1">&#39;y&#39;</span><span class="p">:</span> <span class="p">[</span><span class="mi">1</span><span class="p">,</span> <span class="mi">4</span><span class="p">,</span> <span class="mi">9</span><span class="p">,</span> <span class="mi">16</span><span class="p">]})</span>
<span class="n">tl</span><span class="o">.</span><span class="n">upload_dataset</span><span class="p">(</span><span class="n">df</span><span class="p">,</span> <span class="s2">&quot;my_dataset&quot;</span><span class="p">)</span>
<span class="n">params</span> <span class="o">=</span> <span class="p">{</span>
    <span class="s2">&quot;dataset_id&quot;</span><span class="p">:</span> <span class="s2">&quot;my_dataset&quot;</span><span class="p">,</span>
    <span class="s2">&quot;inputs&quot;</span><span class="p">:</span> <span class="p">[</span><span class="s2">&quot;X&quot;</span><span class="p">],</span>
    <span class="s2">&quot;outputs&quot;</span><span class="p">:</span> <span class="p">[</span><span class="s2">&quot;y&quot;</span><span class="p">],</span>
<span class="p">}</span>
<span class="n">tl</span><span class="o">.</span><span class="n">train_campaign</span><span class="p">(</span><span class="n">params</span><span class="p">,</span> <span class="s2">&quot;my_campaign&quot;</span><span class="p">)</span>
<span class="n">tl</span><span class="o">.</span><span class="n">delete_campaign</span><span class="p">(</span><span class="s2">&quot;my_campaign&quot;</span><span class="p">)</span>
</code></pre>
</div>
</div>


                </section>
    </main>


<style>pre{line-height:125%;}span.linenos{color:inherit; background-color:transparent; padding-left:5px; padding-right:20px;}.pdoc-code .hll{background-color:#ffffcc}.pdoc-code{background:#f8f8f8;}.pdoc-code .c{color:#3D7B7B; font-style:italic}.pdoc-code .err{border:1px solid #FF0000}.pdoc-code .k{color:#008000; font-weight:bold}.pdoc-code .o{color:#666666}.pdoc-code .ch{color:#3D7B7B; font-style:italic}.pdoc-code .cm{color:#3D7B7B; font-style:italic}.pdoc-code .cp{color:#9C6500}.pdoc-code .cpf{color:#3D7B7B; font-style:italic}.pdoc-code .c1{color:#3D7B7B; font-style:italic}.pdoc-code .cs{color:#3D7B7B; font-style:italic}.pdoc-code .gd{color:#A00000}.pdoc-code .ge{font-style:italic}.pdoc-code .gr{color:#E40000}.pdoc-code .gh{color:#000080; font-weight:bold}.pdoc-code .gi{color:#008400}.pdoc-code .go{color:#717171}.pdoc-code .gp{color:#000080; font-weight:bold}.pdoc-code .gs{font-weight:bold}.pdoc-code .gu{color:#800080; font-weight:bold}.pdoc-code .gt{color:#0044DD}.pdoc-code .kc{color:#008000; font-weight:bold}.pdoc-code .kd{color:#008000; font-weight:bold}.pdoc-code .kn{color:#008000; font-weight:bold}.pdoc-code .kp{color:#008000}.pdoc-code .kr{color:#008000; font-weight:bold}.pdoc-code .kt{color:#B00040}.pdoc-code .m{color:#666666}.pdoc-code .s{color:#BA2121}.pdoc-code .na{color:#687822}.pdoc-code .nb{color:#008000}.pdoc-code .nc{color:#0000FF; font-weight:bold}.pdoc-code .no{color:#880000}.pdoc-code .nd{color:#AA22FF}.pdoc-code .ni{color:#717171; font-weight:bold}.pdoc-code .ne{color:#CB3F38; font-weight:bold}.pdoc-code .nf{color:#0000FF}.pdoc-code .nl{color:#767600}.pdoc-code .nn{color:#0000FF; font-weight:bold}.pdoc-code .nt{color:#008000; font-weight:bold}.pdoc-code .nv{color:#19177C}.pdoc-code .ow{color:#AA22FF; font-weight:bold}.pdoc-code .w{color:#bbbbbb}.pdoc-code .mb{color:#666666}.pdoc-code .mf{color:#666666}.pdoc-code .mh{color:#666666}.pdoc-code .mi{color:#666666}.pdoc-code .mo{color:#666666}.pdoc-code .sa{color:#BA2121}.pdoc-code .sb{color:#BA2121}.pdoc-code .sc{color:#BA2121}.pdoc-code .dl{color:#BA2121}.pdoc-code .sd{color:#BA2121; font-style:italic}.pdoc-code .s2{color:#BA2121}.pdoc-code .se{color:#AA5D1F; font-weight:bold}.pdoc-code .sh{color:#BA2121}.pdoc-code .si{color:#A45A77; font-weight:bold}.pdoc-code .sx{color:#008000}.pdoc-code .sr{color:#A45A77}.pdoc-code .s1{color:#BA2121}.pdoc-code .ss{color:#19177C}.pdoc-code .bp{color:#008000}.pdoc-code .fm{color:#0000FF}.pdoc-code .vc{color:#19177C}.pdoc-code .vg{color:#19177C}.pdoc-code .vi{color:#19177C}.pdoc-code .vm{color:#19177C}.pdoc-code .il{color:#666666}</style>
<style>:root{--pdoc-background:#fff;}.pdoc{--text:#212529;--muted:#6c757d;--link:#3660a5;--link-hover:#1659c5;--code:#f8f8f8;--active:#fff598;--accent:#eee;--accent2:#c1c1c1;--nav-hover:rgba(255, 255, 255, 0.5);--name:#0066BB;--def:#008800;--annotation:#007020;}</style>
<style>.pdoc{color:var(--text);box-sizing:border-box;line-height:1.5;background:none;}.pdoc .pdoc-button{cursor:pointer;display:inline-block;border:solid black 1px;border-radius:2px;font-size:.75rem;padding:calc(0.5em - 1px) 1em;transition:100ms all;}.pdoc .pdoc-alert{padding:1rem 1rem 1rem calc(1.5rem + 24px);border:1px solid transparent;border-radius:.25rem;background-repeat:no-repeat;background-position:1rem center;margin-bottom:1rem;}.pdoc .pdoc-alert > *:last-child{margin-bottom:0;}.pdoc .pdoc-alert-note {color:#084298;background-color:#cfe2ff;border-color:#b6d4fe;background-image:url("data:image/svg+xml,%3Csvg%20xmlns%3D%22http%3A//www.w3.org/2000/svg%22%20width%3D%2224%22%20height%3D%2224%22%20fill%3D%22%23084298%22%20viewBox%3D%220%200%2016%2016%22%3E%3Cpath%20d%3D%22M8%2016A8%208%200%201%200%208%200a8%208%200%200%200%200%2016zm.93-9.412-1%204.705c-.07.34.029.533.304.533.194%200%20.487-.07.686-.246l-.088.416c-.287.346-.92.598-1.465.598-.703%200-1.002-.422-.808-1.319l.738-3.468c.064-.293.006-.399-.287-.47l-.451-.081.082-.381%202.29-.287zM8%205.5a1%201%200%201%201%200-2%201%201%200%200%201%200%202z%22/%3E%3C/svg%3E");}.pdoc .pdoc-alert-warning{color:#664d03;background-color:#fff3cd;border-color:#ffecb5;background-image:url("data:image/svg+xml,%3Csvg%20xmlns%3D%22http%3A//www.w3.org/2000/svg%22%20width%3D%2224%22%20height%3D%2224%22%20fill%3D%22%23664d03%22%20viewBox%3D%220%200%2016%2016%22%3E%3Cpath%20d%3D%22M8.982%201.566a1.13%201.13%200%200%200-1.96%200L.165%2013.233c-.457.778.091%201.767.98%201.767h13.713c.889%200%201.438-.99.98-1.767L8.982%201.566zM8%205c.535%200%20.954.462.9.995l-.35%203.507a.552.552%200%200%201-1.1%200L7.1%205.995A.905.905%200%200%201%208%205zm.002%206a1%201%200%201%201%200%202%201%201%200%200%201%200-2z%22/%3E%3C/svg%3E");}.pdoc .pdoc-alert-danger{color:#842029;background-color:#f8d7da;border-color:#f5c2c7;background-image:url("data:image/svg+xml,%3Csvg%20xmlns%3D%22http%3A//www.w3.org/2000/svg%22%20width%3D%2224%22%20height%3D%2224%22%20fill%3D%22%23842029%22%20viewBox%3D%220%200%2016%2016%22%3E%3Cpath%20d%3D%22M5.52.359A.5.5%200%200%201%206%200h4a.5.5%200%200%201%20.474.658L8.694%206H12.5a.5.5%200%200%201%20.395.807l-7%209a.5.5%200%200%201-.873-.454L6.823%209.5H3.5a.5.5%200%200%201-.48-.641l2.5-8.5z%22/%3E%3C/svg%3E");}.pdoc .visually-hidden{position:absolute !important;width:1px !important;height:1px !important;padding:0 !important;margin:-1px !important;overflow:hidden !important;clip:rect(0, 0, 0, 0) !important;white-space:nowrap !important;border:0 !important;}.pdoc h1, .pdoc h2, .pdoc h3{font-weight:300;margin:.3em 0;padding:.2em 0;}.pdoc > section:not(.module-info) h1{font-size:1.5rem;font-weight:500;}.pdoc > section:not(.module-info) h2{font-size:1.4rem;font-weight:500;}.pdoc > section:not(.module-info) h3{font-size:1.3rem;font-weight:500;}.pdoc > section:not(.module-info) h4{font-size:1.2rem;}.pdoc > section:not(.module-info) h5{font-size:1.1rem;}.pdoc a{text-decoration:none;color:var(--link);}.pdoc a:hover{color:var(--link-hover);}.pdoc blockquote{margin-left:2rem;}.pdoc pre{border-top:1px solid var(--accent2);border-bottom:1px solid var(--accent2);margin-top:0;margin-bottom:1em;padding:.5rem 0 .5rem .5rem;overflow-x:auto;background-color:var(--code);}.pdoc code{color:var(--text);padding:.2em .4em;margin:0;font-size:85%;background-color:var(--accent);border-radius:6px;}.pdoc a > code{color:inherit;}.pdoc pre > code{display:inline-block;font-size:inherit;background:none;border:none;padding:0;}.pdoc > section:not(.module-info){margin-bottom:1.5rem;}.pdoc .modulename{margin-top:0;font-weight:bold;}.pdoc .modulename a{color:var(--link);transition:100ms all;}.pdoc .git-button{float:right;border:solid var(--link) 1px;}.pdoc .git-button:hover{background-color:var(--link);color:var(--pdoc-background);}.view-source-toggle-state,.view-source-toggle-state ~ .pdoc-code{display:none;}.view-source-toggle-state:checked ~ .pdoc-code{display:block;}.view-source-button{display:inline-block;float:right;font-size:.75rem;line-height:1.5rem;color:var(--muted);padding:0 .4rem 0 1.3rem;cursor:pointer;text-indent:-2px;}.view-source-button > span{visibility:hidden;}.module-info .view-source-button{float:none;display:flex;justify-content:flex-end;margin:-1.2rem .4rem -.2rem 0;}.view-source-button::before{position:absolute;content:"View Source";display:list-item;list-style-type:disclosure-closed;}.view-source-toggle-state:checked ~ .attr .view-source-button::before,.view-source-toggle-state:checked ~ .view-source-button::before{list-style-type:disclosure-open;}.pdoc .docstring{margin-bottom:1.5rem;}.pdoc section:not(.module-info) .docstring{margin-left:clamp(0rem, 5vw - 2rem, 1rem);}.pdoc .docstring .pdoc-code{margin-left:1em;margin-right:1em;}.pdoc h1:target,.pdoc h2:target,.pdoc h3:target,.pdoc h4:target,.pdoc h5:target,.pdoc h6:target,.pdoc .pdoc-code > pre > span:target{background-color:var(--active);box-shadow:-1rem 0 0 0 var(--active);}.pdoc .pdoc-code > pre > span:target{display:block;}.pdoc div:target > .attr,.pdoc section:target > .attr,.pdoc dd:target > a{background-color:var(--active);}.pdoc *{scroll-margin:2rem;}.pdoc .pdoc-code .linenos{user-select:none;}.pdoc .attr:hover{filter:contrast(0.95);}.pdoc section, .pdoc .classattr{position:relative;}.pdoc .headerlink{--width:clamp(1rem, 3vw, 2rem);position:absolute;top:0;left:calc(0rem - var(--width));transition:all 100ms ease-in-out;opacity:0;}.pdoc .headerlink::before{content:"#";display:block;text-align:center;width:var(--width);height:2.3rem;line-height:2.3rem;font-size:1.5rem;}.pdoc .attr:hover ~ .headerlink,.pdoc *:target > .headerlink,.pdoc .headerlink:hover{opacity:1;}.pdoc .attr{display:block;margin:.5rem 0 .5rem;padding:.4rem .4rem .4rem 1rem;background-color:var(--accent);overflow-x:auto;}.pdoc .classattr{margin-left:2rem;}.pdoc .name{color:var(--name);font-weight:bold;}.pdoc .def{color:var(--def);font-weight:bold;}.pdoc .signature{background-color:transparent;}.pdoc .param, .pdoc .return-annotation{white-space:pre;}.pdoc .signature.multiline .param{display:block;}.pdoc .signature.condensed .param{display:inline-block;}.pdoc .annotation{color:var(--annotation);}.pdoc .view-value-toggle-state,.pdoc .view-value-toggle-state ~ .default_value{display:none;}.pdoc .view-value-toggle-state:checked ~ .default_value{display:inherit;}.pdoc .view-value-button{font-size:.5rem;vertical-align:middle;border-style:dashed;margin-top:-0.1rem;}.pdoc .view-value-button:hover{background:white;}.pdoc .view-value-button::before{content:"show";text-align:center;width:2.2em;display:inline-block;}.pdoc .view-value-toggle-state:checked ~ .view-value-button::before{content:"hide";}.pdoc .inherited{margin-left:2rem;}.pdoc .inherited dt{font-weight:700;}.pdoc .inherited dt, .pdoc .inherited dd{display:inline;margin-left:0;margin-bottom:.5rem;}.pdoc .inherited dd:not(:last-child):after{content:", ";}.pdoc .inherited .class:before{content:"class ";}.pdoc .inherited .function a:after{content:"()";}.pdoc .search-result .docstring{overflow:auto;max-height:25vh;}.pdoc .search-result.focused > .attr{background-color:var(--active);}.pdoc .attribution{margin-top:2rem;display:block;opacity:0.5;transition:all 200ms;filter:grayscale(100%);}.pdoc .attribution:hover{opacity:1;filter:grayscale(0%);}.pdoc .attribution img{margin-left:5px;height:35px;vertical-align:middle;width:70px;transition:all 200ms;}.pdoc table{display:block;width:max-content;max-width:100%;overflow:auto;margin-bottom:1rem;}.pdoc table th{font-weight:600;}.pdoc table th, .pdoc table td{padding:6px 13px;border:1px solid var(--accent2);}</style></div>