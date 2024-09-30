

function addToConversationHistory(question, answer, evaluation) {
    const historyDiv = document.getElementById('conversation-history');
    const qaPair = document.createElement('div');
    qaPair.className = 'qa-pair';
    qaPair.innerHTML = `
        <p><strong>Q:</strong> ${question}</p>
        <p><strong>A:</strong> ${answer}</p>
        <p><strong>Evaluation:</strong> ${JSON.stringify(evaluation, null, 2)}</p>
    `;
    historyDiv.appendChild(qaPair);
    log('Conversation history updated');
}

