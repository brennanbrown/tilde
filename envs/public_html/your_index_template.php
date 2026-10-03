<!--
hey,
this is a template for your own index.php.
you can edit this file and rename it to index.php.
have fun!

cp ~/public_html/your_index_template.php ~/public_html/index.php

YOU CAN REMOVE THIS COMMENT!
-->

<?php $user = posix_getpwuid(fileowner(__FILE__))["name"]; ?>
<!-- HTML HEADER -->
<!DOCTYPE html>
<html lang="en">
	<head>
		<title>~<?=$user?> on envs.net</title>
		<meta http-equiv="content-type" content="text/html; charset=utf-8" />
		<meta name="author" content="<?=$user?>">
		<meta name="robots" content="noindex,nofollow">
		<meta name="description" content="~<?=$user?> on envs.net" />
		<meta name="keywords" content="<?=$user?>" />
		<meta name="viewport" content="width=device-width, initial-scale=1" />
		<link rel="stylesheet" href="https://envs.net/css/neoenvs.css" />
		<link rel="stylesheet" href="https://envs.net/css/fork-awesome.min.css" />
	</head>
	<body id="body" class="dark-mode">

	<main>
		<div class="block">
			<h1><?=$user?></h1>
		</div>

		<p>hi and welcome to my new website.</p>

		<table>
	  		<tr><th></th> <th></th></tr>
	  		<tr>
	    		<td>IRC:</td>
	    		<td><?=$user?> on tilde.chat</td>
	  		</tr>
	  		<tr>
	    		<td>Mail:</td>
	    		<td><code><?=$user?>&#64;envs.net</code></td>
	  		</tr>
		</table>

	</main>

<!-- You can also enable a right sidebar -->
<!-- SIDEBAR -->
<!--
	<div id="sidebar">

		<nav class="block">
			<p>
				more text
			</p>
		</nav>
	</div>
-->
</html>
