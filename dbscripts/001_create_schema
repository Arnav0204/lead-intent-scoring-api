

CREATE TABLE offers(
    offer_id BIGSERIAL NOT NULL,
    name VARCHAR(255) NOT NULL,
    value_props JSONB DEFAULT '[]'::JSONB,
    ideal_use_cases JSONB DEFAULT '[]'::JSONB,
    created_at TIMESTAMP DEFAULT NOW(),
    CONSTRAINT pk_offers_offer_id PRIMARY KEY (offer_id)
);

CREATE TABLE leads(
    lead_id BIGSERIAL NOT NULL,
    name VARCHAR(255) NOT NULL,
    role VARCHAR(255),
    company VARCHAR(255),
    industry VARCHAR(255),
    location VARCHAR(255),
    linkedin_bio TEXT,
    offer_id BIGINT NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    CONSTRAINT pk_leads_lead_id PRIMARY KEY (lead_id),
    CONSTRAINT fk_leads_offer_id FOREIGN KEY (offer_id) 
        REFERENCES offers(offer_id) ON DELETE CASCADE
);

CREATE TABLE scores(
    score_id BIGSERIAL NOT NULL,
    total_score INT NOT NULL,
    intent VARCHAR(50) NOT NULL,        
    reasoning TEXT NOT NULL,  
    offer_id BIGINT NOT NULL,
    lead_id BIGINT NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    CONSTRAINT pk_scores_score_id PRIMARY KEY (score_id),
    CONSTRAINT fk_scores_offer_id FOREIGN KEY (offer_id)
        REFERENCES offers(offer_id) ON DELETE CASCADE
    CONSTRAINT fk_scores_lead_id FOREIGN KEY (lead_id)
        REFERENCES leads(lead_id) ON DELETE CASCADE
);