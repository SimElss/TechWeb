// Fonction pour acheter un objet
async function buyItem(itemId) {
    try {
        const response = await fetch(`/buy/${itemId}`, {
            method: 'POST',
            // autres options de requête...
        });
        const data = await response.json();
        // Vérifie si la réponse contient une erreur
        if (response.status === 200) {
            // L'achat a réussi
            alert('Objet acheté avec succès !');
            // Actualiser la page ou effectuer d'autres actions nécessaires
        } else {
            // Afficher un message d'erreur si l'objet est déjà dans la table d'association
            if (data.error === 'already_in_cart') {
                alert('Cet objet est déjà dans votre panier.');
            } else {
                // Autre gestion des erreurs
                alert('Une erreur s\'est produite lors de l\'achat de cet objet.');
            }
        }
    } catch (error) {
        // Gestion des erreurs
        console.error('Une erreur s\'est produite :', error);
        alert('Une erreur s\'est produite. Veuillez réessayer plus tard.');
    }
}
