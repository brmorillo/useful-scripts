<?php

require 'vendor/autoload.php';

use PhpOffice\PhpSpreadsheet\IOFactory;

// Ler dados do arquivo Excel
$inputFileName = 'Book1.xlsx';
$spreadsheet = IOFactory::load($inputFileName);

// Obter dados da planilha
$worksheet = $spreadsheet->getActiveSheet();
$rows = $worksheet->toArray();

// Converter dados para um array associativo
$data = [];
foreach ($rows as $row) {
    $estado = $row[0];
    $cidade = $row[1];
    if (!isset($data[$estado])) {
        $data[$estado] = [];
    }
    $data[$estado][] = $cidade;
}

// Converter array para JSON
$json = json_encode($data);

// Imprimir JSON
echo $json;
