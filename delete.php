<?php
// Připojení k databázi pomocí funkce .
require_once "functions.php"; 

// Pokud nění uživatel přihlášen tak nemůže smazat záznam.
if (!isset($_SESSION['admin'])) {
    echo '<script language="javascript">';
    echo 'alert("Neoprávněný přístup!")';
    echo '</script>';

}

// Na jaký záznam se klikne tak vezme user_id z databáze 1AUsers a smaže to ten záznam.
if (isset($_GET['id'])) {
    $user_id = intval($_GET['id']);

    $sql = "DELETE FROM 1AUsers WHERE user_id = ?";
    $stmt = $conn->prepare($sql);
    $stmt->bind_param("i", $user_id);

    if ($stmt->execute()) {
        echo '<script language="javascript">';
        echo 'alert("Záznam smazán.")';
        echo '</script>';
    } else {
        echo "Chyba při mazání: " . $conn->error;
    }

    $stmt->close();
}

// Po smazání to vrátí na hlavní stránku.
header("Location: index.php");
exit();
?>
