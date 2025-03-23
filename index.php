<?php

// Spustí se sekce.
session_start();

// Připojení souboru s funkcemi
include "functions.php"; 

/**
 * Zpracování přihlašovacího formuláře
 * Pokud je metoda požadavku POST a jsou odeslány hodnoty username a password,
 * provede se ověření přihlašovacích údajů.
 */

// Podmínky pro přihlášení, pokud se uživatel jmenuje admin a heslo je admin tak to přihlásí do session. Pokud je špatně přihlášení tak to nepřihlásí a napíše to.
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    if(isset($_POST['username']) && isset($_POST["password"])){
        $username = trim($_POST["username"]);
        $password = trim($_POST["password"]);
    
        // Ověření správnosti přihlašovacích údajů
        if ($username === "admin" && $password === "admin") {
            $_SESSION["admin"] = true;
            header("Location: index.php"); // Přesměrování na hlavní stránku
            echo "Byl jsi přihlášen.";
        } else {
            echo("Špatné jméno nebo heslo!"); // Chybová zpráva při špatném přihlášení
        }
    }
}

/**
 * Odhlášení uživatele
 * Pokud je v URL parametr logout, provede se zrušení session
 * a přesměrování na hlavní stránku.
 */

// Když uživatel klikne na tlačítko odhlásit tak to odhlásí uživatele, smaže session a vrátí na hlavní stránku.
if (isset($_GET["logout"])) {
    session_start(); // Přidáno pro jistotu, pokud session není spuštěná
    session_unset(); // Odstraní všechny session proměnné
    session_destroy(); // Zničí session
    header("Location: index.php"); // Přesměrování na hlavní stránku
    exit();
}

    /**
     * SQL dotaz pro získání seznamu uživatelů a jejich nejvyššího skóre
     * Data se získávají z tabulek 1AUsers a 1AScores
     * Výstup je setříděný sestupně podle skóre.
     */
    $sql = "SELECT u.user_id, u.username, MAX(s.score) AS score
            FROM 1AUsers u
            INNER JOIN 1AScores s ON u.user_id = s.user_id
            GROUP BY u.user_id, u.username
            ORDER BY score DESC;";

    $result = $conn->query($sql);// Provedení dotaz

?>


<!DOCTYPE html>
<html lang="cs">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="author" content="Radovan Todorov">
    <title>The Best Pong On Earth</title>
    <style>
        body {
            font-family: Arial, sans-serif; /* Nastavení základního písma */
            background: linear-gradient(135deg, #1a1a2e, #16213e); /* Barevný přechod pozadí */
            color: white; /* Barva textu */
            text-align: center; /* Zarovnání textu na střed */
            margin: 0;
            padding: 0;
        }

        .container {
            width: 60%; /* Šířka hlavního kontejneru */
            margin: 5% auto; /* Zarovnání na střed s horním okrajem */
            background: rgba(255, 255, 255, 0.1); /* Průhledné pozadí */
            padding: 30px; /* Vnitřní odsazení */
            border-radius: 15px; /* Zaoblené rohy */
            box-shadow: 0px 0px 20px rgba(0, 0, 0, 0.5); /* Stín okolo */
            backdrop-filter: blur(10px); /* Rozmazání pozadí */
            opacity: 0;
            transform: translateY(-20px);
            animation: fadeIn 1s forwards;
        }

        @keyframes fadeIn {
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        @keyframes fadeIn {
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        h1 {
            font-size: 2.5em; /* Velikost nadpisu */
            background: linear-gradient(45deg, #ff512f, #dd2476); /* Barevný efekt textu */
            background-clip: text; /* Standardní vlastnost */
            -webkit-background-clip: text; /* Pro WebKit prohlížeče */
            color: transparent;
        }

        .hidden {
            display: none; /* Skrytý prvek */
        }

        .fade {
            opacity: 0;
            transform: scale(0.95);
            transition: opacity 0.5s ease, transform 0.5s ease;
        }
        .fade.show {
            opacity: 1;
            transform: scale(1);
        }

        button {
            padding: 12px 25px; /* Větší tlačítka pro lepší viditelnost */
            margin: 15px;
            border: none;
            cursor: pointer;
            font-size: 18px;
            font-weight: bold;
            border-radius: 25px; /* Zaoblené rohy tlačítka */
            transition: 0.3s;
        }

        .btn-login {
            background: linear-gradient(90deg, #28a745, #218838); /* Zelené tlačítko */
            color: white;
        }
        .btn-login:hover {
            background: #1e7e34;
            transform: scale(1.05);
        }
        
        .btn-logout {
            background: linear-gradient(90deg, #dc3545, #c82333); /* Červené tlačítko */
            color: white;
        }
        .btn-logout:hover {
            background: #bd2130;
            transform: scale(1.05);
        }

        .input-box {
            padding: 12px;
            margin: 10px;
            width: 80%;
            border: none;
            border-radius: 8px;
            font-size: 16px;
            text-align: center;
            background: rgba(255, 255, 255, 0.2);
            color: white;
            outline: none;
            transition: 0.3s;
        }
        .input-box:focus {
            background: rgba(255, 255, 255, 0.4);
        }

        img {
            width: 40%;
            border-radius: 15px;
            margin: 20px 0;
            box-shadow: 0px 0px 15px rgba(255, 255, 255, 0.2);
        }
        table {
            width: 80%;
            margin: 20px auto;
            border-collapse: collapse;
            background-color: #0f3460; /* Tmavě modré pozadí tabulky */
            box-shadow: 0 0 15px rgba(0, 255, 255, 0.3); /* Neonový efekt */
    }

        td {
            border: 2px solid #1a1a2e; /* Tmavý rámeček */
            padding: 10px;
            text-align: center;
            color: white;
        }

        th {
            background-color:rgb(170, 3, 30); /* Červena hlavička tabulky */
            color: white;
            font-weight: bold;
            padding: 12px;
            text-transform: uppercase;
        }

        tr:nth-child(even) {
            background-color: #16213e; /* Střídavě tmavě modré řádky */
}

        tr:hover {
            background-color:rgba(43, 255, 0, 0.14); /* Při najetí oranžové zvýraznění */
            color: white;
}

        .containe {
            display: flex;
            flex-direction: column;
            align-items: center;
            margin-top: 20px;
            width: 100%;
            padding: 0 10px;
    }
    #admin-login-modal {
        position: fixed;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        background: rgba(0, 0, 0, 0.8);
        padding: 20px;
        border-radius: 10px;
        display: none;
        z-index: 2000;
    }

    .admin-modal-content {
        background: rgba(255, 255, 255, 0.2);
        padding: 20px;
        border-radius: 10px;
        text-align: center;
    }

    .admin-login-btn {
        position: fixed;
        top: 10px;
        right: 10px;
        background: linear-gradient(90deg, #ff512f, #dd2476);
        color: white;
        padding: 10px 15px;
        border: none;
        cursor: pointer;
        font-size: 16px;
        font-weight: bold;
        border-radius: 8px;
        transition: 0.3s;
        z-index: 1000; /* Aby bylo vždy nad ostatním obsahem */
    }

    .admin-login-btn:hover {
        background: #bd2130;
        transform: scale(1.1);
    }

    .image-container {
        text-align: center;
        margin: 30px 0;
    }

    .image-container img {
        width: 35%; /* Menší velikost obrázků */
        max-width: 500px; /* Maximální šířka pro lepší vzhled */
        border-radius: 15px;
        box-shadow: 0px 0px 15px rgba(255, 255, 255, 0.2);
        transition: transform 0.3s ease;
        display: block;
        margin: 15px auto;
    }

    .image-container img:hover {
        transform: scale(1.20);
    }

    .orange-box {
        border: 3px solid orange; /* Oranžový rámeček */
        padding: 15px; /* Vnitřní okraj */
        border-radius: 10px; /* Zaoblené rohy */
        background-color: rgba(255, 165, 0, 0.1); /* Světle oranžové pozadí */
        color: white; /* Bílý text pro lepší čitelnost */
        font-family: Arial, sans-serif; /* Pěkné písmo */
        text-align: center; /* Zarovnání na střed */
        width: 60%; /* Šířka 60% obrazovky */
        margin: 20px auto; /* Zarovnání na střed */
        box-shadow: 0px 0px 15px rgba(255, 140, 0, 0.4); /* Jemný oranžový stín */
    }
    </style>
</head>
<body>

    <!-- Tlačítko pro přihlášení admina -->
    <button class="admin-login-btn" onclick="showAdminLogin()">🔑 Admin</button>

    <?php if (isset($_SESSION["admin"])): ?>
        <!-- Tlačítko pro odhlášení admina -->
        <button class="btn-logout" onclick="window.location.href='index.php?logout=true'">🚪 Odhlásit</button>
    <?php endif; ?>

    <div class="container" id="main-container">
    <h1>The Best Pong On Earth</h1>
    <p>Klasická hra Pong s AI a PvP!</p>

    <!-- Přihlašovací formulář pro admina -->
    <div id="admin-login-modal" class="hidden">
        <div class="admin-modal-content">
            <h2>Admin Přihlášení</h2>
            <form method="POST">

                <!-- Pole pro zadání uživatelského jména -->
                <input type="text" name="username" class="input-box" placeholder="Uživatelské jméno">

                <!-- Pole pro zadání hesla -->
                <input type="password" name="password" class="input-box" placeholder="Heslo">
                <br>

                <!-- Tlačítko pro přihlášení -->
                <button type="submit" class="btn-login">Přihlásit</button>

                <!-- Tlačítko pro zavření okna -->
                <button type="button" class="btn-logout" onclick="hideAdminLogin()">Zavřít</button>
            </form>
        </div>
    </div>

    <?php if (!isset($_SESSION["admin"]) && !isset($_SESSION["user"])): ?>
    <!-- Sekce pro běžné přihlášení uživatele -->
        <div id="auth-section" class="fade show">
            <h2>Přihlášení</h2>

            <!-- Pole pro zadání uživatelského jména -->
            <input type="text" id="login-username" class="input-box" placeholder="Uživatelské jméno">
            
            <!-- Pole pro zadání hesla -->
            <input type="password" id="login-password" class="input-box" placeholder="Heslo">
            <br>

            <!-- Tlačítko pro přihlášení -->
            <button class="btn-login" onclick="login()">Přihlásit se</button>

            <!-- Odkaz na registraci pro nové uživatele -->
            <p>Nemáte účet? <a href="#" onclick="showRegister()" style="color: orange;">Zaregistruj se</a></p>
        </div>
    <?php endif; ?>

    <!-- Sekce pro registraci nového uživatele -->
    <div id="register-section" class="hidden">
        <h2>Registrace</h2>

        <!-- Pole pro zadání nového uživatelského jména -->
        <input type="text" id="register-username" class="input-box" placeholder="Zvolte uživatelské jméno">

        <!-- Pole pro zadání nového hesla -->
        <input type="password" id="register-password" class="input-box" placeholder="Zvolte heslo">
        <br>

        <!-- Tlačítko pro registraci -->
        <button class="btn-login" onclick="register()">Registrovat</button>

        <!-- Odkaz pro přepnutí zpět na přihlášení -->
        <p>Již máte účet? <a href="#" onclick="showLogin()" style="color: yellow;">Přihlaste se</a></p>
    </div>

    <div id="user-content" class="">
        <h2>Vítejte <span id="username-display"></span>!</h2>
        <!-- Tabulka se záznamy hráčů a jejich skóre-->
<div class="container w-50 p-4">
        <table class="table table-bordered table-striped">
            <thead>
                <tr class="table-primary">
                <th scope="col">Jméno: </th>
                <th scope="col">Skóre: </th>
                <!-- Sloupec se zobrazí zda-li je uživatel přihlášený jako admin.-->
                <?php if (isset($_SESSION["admin"])): ?> <th>Smazání záznamu</th> <?php endif; ?>
                </tr>
            </thead>
            <?php
            // Bere data z databáze a bude to probíhat dokud budou záznamy v databázi.
            if ($result->num_rows > 0) {
                while ($row = $result->fetch_assoc()) {
                    echo "<tr>
                            <td>" . htmlspecialchars($row["username"]) . "</td>
                            <td>" . htmlspecialchars($row["score"]) . "</td>";
                    // Zobrazí se zda-li je uživatel přihlášený.
                    if (isset($_SESSION["admin"])) {
                        echo "<td><a href='delete.php?id=" . $row["user_id"] . "' onclick='return confirm(\"Opravdu chcete smazat tento záznam?\")' class='text-danger becko'>❌</a></td>";
                    }
                    echo "</tr>";
                }
                // Zda-li nejsou data v databázi tak to vypíše níže. 
            } else {
                echo "<tr><td colspan='3'>Žádná data</td></tr>";
            }
            ?>
            </tbody>
        </table>
    </div>

    <hr>

    <div class="orange-box">
        <h2>Popis programu (Pong hra)</h2>
        <p>
            Tento program je <b>Pong hra</b>, která byla napsána v Pythonu s použitím Pygame a PyQt. <br>
            Hráč si může vybrat mezi dvěma herními režimy: <br><br>

            <b>Hráč vs. Počítač</b> – hráč hraje proti AI. <br>
            <b>Hráč vs. Hráč</b> – dva hráči proti sobě na jednom zařízení. <br><br>

            <b>Hra zahrnuje:</b> <br>
            - Přihlašování uživatelů přes Pygame UI. <br>
            - Dynamické menu s možností výběru herního režimu. <br>
            - Zobrazení výsledků pomocí PyQt zpráv. <br>
        </p>
    </div>

        <h2>Seznam funkcí hry:</h2>  <!-- Nadpis pro seznam funkcí -->
        <ul>
            <li><b>M</b>ožnost hry proti AI(zapisuje skóre do txt souboru, do databaze a následně na web), pvp(zapisuje do txt souboru)</li>  <!-- Funkce 0 -->
            <li><b>K</b>aždý hráč může mít více záznamů v tabulce skore , což odpovídá vztahu 1:N</li>  <!-- Funkce 1 -->
            <li><b>U</b>kládání skóre hráčů do txt souboru a do databáze</li> <!-- Funkce 2 --> 
            <li><b>AI</b> využívá algoritmus sledování míčku</li> <!-- Funkce 3 -->
            <li><b>P</b>řihlášení uživatele</li>  <!-- Funkce 4 -->
            
        </ul>

        <h2>Algoritmy a knihovny:</h2>  <!-- Nadpis pro algoritmy a knihovny -->
        <ul>
            <li><b>Knihovny:</b> Pygame, PyQt5, Mariadb, sys, re, random(randint)</li>  <!-- Seznam knihoven -->
            <li><b>AI Algoritmus:</b> Sledování pozice míčku</li>  <!-- Seznam AI algoritmů -->
            <li><b>Kolize:</b> Detekce kolize míčku s hráčem a zdmi</li>  <!-- Seznam kolizních detekcí -->
            <li><b>Smart_ai:</b> Algoritmus pohybu míčku</li>  
            <li><b>Dynamická změna obtížnosti:</b> Zvyšování rychlosti míčku</li>  
            <li><b>Databáze MariaDB:</b> Ukládání a načítaní skóre hráču</li>
            <li><b>Ukládání skóre do txt souboru:</b> Čte, zapisuje a aktualizuje skóre. Používá řazení sorting, uchovává pouze TOP 10 skóre</li>


        </ul>

        <div class="image-container">
            <h2>ER Diagram</h2>
            <img src="erdiagram.png" alt="ER Diagram">

            <h2>Vývojový Diagram</h2>
            <img src="Vdiagram.png" alt="Vývojový Diagram">
        </div>

        <h2>Autoři:</h2>  <!-- Nadpis pro autory -->
        <p>Jméno autora: (Radovan Todorov)</p>  <!-- Jméno autora -->

        <h2>Odkaz na stažení:</h2>  <!-- Nadpis pro GitHub odkaz -->
        <!-- Odkaz na GitHub repo -->
        <a href="https://github.com/RadovanTKM/programko_maturita/tree/main" target="_blank" style="color: #39FF14;">GitHub Repozitář</a>

        <br><br>
        <button class="btn-logout" onclick="logout()">Odhlásit se</button>
    </div>
</div>


<script>
    /**
     * Zobrazí okno pro přihlášení admina.
     */
    function showAdminLogin() {
    document.getElementById("admin-login-modal").style.display = "block";
    }

    /**
     * Skryje okno pro přihlášení admina.
     */
    function hideAdminLogin() {
        document.getElementById("admin-login-modal").style.display = "none";
    }

    /**
     * Zobrazí okno pro přihlášení admina a posune stránku na toto okno.
     */
    function showAdminLogin() {
        let modal = document.getElementById("admin-login-modal");
        modal.style.display = "block";
        modal.scrollIntoView({ behavior: "smooth", block: "center" });
    }

    /**
     * Zobrazí registrační sekci a skryje sekci pro přihlášení.
     */
    function showRegister() {
        document.getElementById("auth-section").classList.add("hidden");
        document.getElementById("register-section").classList.remove("hidden");
        document.getElementById("register-section").classList.add("show");
    }

    /**
     * Zobrazí sekci pro přihlášení a skryje registrační sekci.
     */
    function showLogin() {
        document.getElementById("auth-section").classList.remove("hidden");
        document.getElementById("register-section").classList.add("hidden");
    }

    /**
     * Umožňuje registraci uživatele.
     * Uloží uživatelské jméno a heslo do localStorage,
     * pokud uživatel ještě neexistuje.
     */
    function register() {
        let username = document.getElementById("register-username").value;
        let password = document.getElementById("register-password").value;
        if (username === "" || password === "") {
            alert("Vyplňte všechna pole!");
            return;
        }
        if (localStorage.getItem(username)) {
            alert("Tento uživatel již existuje!");
            return;
        }
        localStorage.setItem(username, password);
        alert("Registrace úspěšná! Nyní se můžete přihlásit.");
        showLogin();
    }

    /**
     * Přihlásí uživatele ověřením jeho jména a hesla uloženého v localStorage.
     */
    function login() {
        let username = document.getElementById("login-username").value;
        let password = document.getElementById("login-password").value;
        let storedPassword = localStorage.getItem(username);
        if (!storedPassword) {
            alert("Uživatel neexistuje! Nejprve se registrujte.");
            return;
        }
        if (storedPassword !== password) {
            alert("Špatné heslo!");
            return;
        }
        localStorage.setItem("loggedInUser", username);
        checkLogin();
    }

    /**
     * Odhlásí uživatele odstraněním jeho jména ze session (localStorage).
     */
    function logout() {
        localStorage.removeItem("loggedInUser");
        checkLogin();
    }

    /**
     * Kontroluje, zda je uživatel přihlášen,
     * a podle toho zobrazuje nebo skrývá příslušné sekce na stránce.
     */
    function checkLogin() {
        let loggedInUser = localStorage.getItem("loggedInUser");
        if (loggedInUser) {
            document.getElementById("username-display").innerText = loggedInUser;
            document.getElementById("auth-section").classList.add("hidden");
            document.getElementById("register-section").classList.add("hidden");
            document.getElementById("user-content").classList.remove("hidden");
        } else {
            document.getElementById("auth-section").classList.remove("hidden");
            document.getElementById("user-content").classList.add("hidden");
        }
    }

    checkLogin();
</script>
    <!-- Ukončení spojeni s databází-->
    <?php $conn -> close();?>
    </main>
    <!-- Footer, kde se bude měnit rok automaticky.-->
    <footer>
        <div class="text-center p-3" style="background-color: rgba(0,0,0,0.05)">&copy; <?php echo date("Y"); ?> Radovan Todorov, všechna práva vyhrazena.</div>
    </footer>
</body>
</html>