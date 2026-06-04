export const StripeServices = {
    stripe: null,
    elements: null,
    cardElement: null,

    /**
     * Inicializa Stripe y monta el card element
     * @param {string} publicKey
     * @param {string} cardContainerId - acepta "id" o "#id"
     */
    initialize(publicKey, cardContainerId) {
        this.stripe = Stripe(publicKey);
        this.elements = this.stripe.elements();

        this.cardElement = this.elements.create("card", {
            style: {
                base: {
                    fontSize: "16px",
                    color: "#32325d",
                    "::placeholder": { color: "#aab7c4" }
                }
            }
        });

        if (!cardContainerId) {
            console.error("StripeServices: cardContainerId no definido");
            return;
        }

        // 🔥 NORMALIZAR ID (quita # si viene incluido)
        const normalizedId = cardContainerId.startsWith("#")
            ? cardContainerId.slice(1)
            : cardContainerId;

        const container = document.querySelector(`#${normalizedId}`);

        if (!container) {
            console.error(`StripeServices: no se encontró el elemento #${normalizedId}`);
            return;
        }

        this.cardElement.mount(container);
    },

    async createToken() {
        if (!this.stripe || !this.cardElement) {
            throw new Error("Stripe no inicializado");
        }

        const result = await this.stripe.createToken(this.cardElement);

        if (result.error) {
            throw result.error;
        }

        return result.token.id;
    },

    clear() {
        if (this.cardElement) {
            this.cardElement.clear();
        }
    }
};